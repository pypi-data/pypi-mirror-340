import json
from dataclasses import dataclass, field
from typing import ClassVar
from pathlib import Path
from uuid import uuid4
from time import sleep

# from ceon_render import file_reference
from ceon_render.file_reference import CeonFileReference
from ceon_render import render_app
from ceon_render import render_provider
from ceon_render import render_pipeline

# from ceon_render import render_job

from ceon_render.render_providers.conductor.render_provider_conductor import (
    RenderProviderConductor,
    RenderProviderConductorConfig,
)
from ceon_render.render_providers.local import RenderProviderLocal

from ceon_render import render_apps


CSTOCK_LIB_DIR = "/mnt/FileStorage/Dayne/Web/proj_ceonstock/assets/python"
PROJECT_DIR = str(
    Path(
        "/mnt/FileStorage/Dayne/Web/proj_ceonstock/local_storage/projects/e8bdd183-fd0e-408d-9c38-e375f735925a"
    )
)
HIPFILE = str(Path(PROJECT_DIR, "hou_project/waving_flag_15_hda_embed.hiplc"))
# temp_uuid = str(uuid4())
temp_uuid = "296842ea-a037-4138-8b83-0ebb98510e0a"
JOB_DIR = (
    f"/mnt/FileStorage/Dayne/Web/proj_ceonstock/local_storage/jobs/{temp_uuid}"
)
OUT_DIR = str(Path(JOB_DIR, "job_outputs"))


def register_apps():
    render_app.register(render_apps.AppRenderJobHou)
    render_app.register(render_apps.AppRenderJobFFmpeg)


def register_providers():
    render_provider.register(
        RenderProviderLocal(api_url="http://localhost:3263")
    )
    render_provider.register(RenderProviderConductor())


def main():
    register_apps()
    register_providers()
    # pipeline_job = render_pipeline.CeonRenderPipelineJob(
    #     job_name="render_hou_frames",
    #     app_type="hou",
    #     app_version="20.0.547",
    #     app_render_settings={
    #         "target_node": "/out/karma_cpu",
    #         "node_type": "karma_cpu",
    #     },
    #     job_input=CeonFileReference(target="hou_proj/simple_box.hiplc"),
    #     job_output="output.$F4.exr",
    # )
    # print(pipeline_job)
    env = {
        "CSTOCK": JOB_DIR,
        # point to the ceonstock root dir that contains the ceonstock folder,
        # but do not upload the other files in the parent folder because .git causes upload failures
        "CSTOCK_LIB": str(CSTOCK_LIB_DIR),
    }
    upload_paths = [
        PROJECT_DIR,
        HIPFILE,
        f"{CSTOCK_LIB_DIR}/ceonstock/ceonstock",
        f"{CSTOCK_LIB_DIR}/ceon_render/ceon_render",
        f"{JOB_DIR}/ceonstock_job.json",
        f"{JOB_DIR}/job_inputs",
    ]
    for path in upload_paths:
        if not Path(path).exists():
            raise Exception(f"Missing local path: {path}")
    hou_render_job = render_apps.AppRenderJobHou(
        hipfile=HIPFILE,
        target_node="/out/karma1",
        node_type="karma_cpu",
        output_file=f"{OUT_DIR}/output.$F4.exr",
        frame_dimensions=(960, 540),
        frame_range=(1, 5, 1),
        env=env,
    )
    ffmpeg_xcode_job = render_apps.AppRenderJobFFmpeg(
        input_file=f"{OUT_DIR}/output.%04d.exr",
        output_file=f"{OUT_DIR}/xcoded.mp4",
    )

    jobs = [hou_render_job, ffmpeg_xcode_job]
    grouped_jobs = render_pipeline.group_jobs_by_render_provider(
        jobs, allowed_providers=["conductor", "local"]
    )
    print("grouped jobs:")
    for job_group in grouped_jobs:
        print(job_group)

    print("Submitting hybrid provider test...")
    jobs_lookup = {}
    for job in jobs:
        jobs_lookup[job.job_name] = job
    if len(jobs_lookup.keys()) != len(jobs):
        raise Exception(
            "Length missmatch when building lookup dict for jobs. \
Most likely due to a duplicate job name overwriting an existing value"
        )

    for job_group in grouped_jobs:
        render_provider_name = job_group["render_provider"]
        jobs_to_submit = [
            jobs_lookup[job_name] for job_name in job_group["job_names"]
        ]
        # Currently submitting one-by-one because CONDUCTER does nto handle dependencies.
        # TODO module/library to handle multi-step submission tracking?

        for job in jobs_to_submit:
            submit_and_wait_for_job(
                job,
                render_provider_name=render_provider_name,
                upload_paths=upload_paths,
            )


def submit_and_wait_for_job(
    app_render_job: render_app.AppRenderJob,
    render_provider_name: str,
    upload_paths: list[str],
):
    print()
    print("Submitting job...")
    provider = render_provider.get(render_provider_name)
    render_provider_config = None
    if render_provider_name == "conductor":
        render_provider_config = RenderProviderConductorConfig(
            batch_size=2,
            upload_paths=upload_paths,
            job_title="hda without spare parameters",
        )
    provider_job_uuid = provider.submit_job(
        app_render_job, render_provider_config=render_provider_config
    )
    print(
        f"Submitted job {temp_uuid} to provider with provider job uuid: {provider_job_uuid}"
    )

    print(
        f"Waiting for provider '{render_provider_name}' job {provider_job_uuid}..."
    )
    provider.wait_for_job_completion(provider_job_uuid)

    print(f"Downloading results for provider job: {provider_job_uuid}...")
    downloaded_results = provider.download_job_outputs(provider_job_uuid)
    return downloaded_results


if __name__ == "__main__":
    main()
