"""
模块名称: Stable Diffusion 运行脚本 (Stable Diffusion Runner)
文件用途:
    调用本地或远程的 Stable Diffusion 模型，根据生成的提示词 (ai_prompt.py) 生成高质量插画。

    注意:
    - 需要 NVIDIA 显卡 (CUDA 支持)。
    - 需要安装 pytorch 和 diffusers 库。
    - 此脚本属于高级扩展功能，非核心像素生成链路的一部分。
"""

import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from .ai_prompt import build_prompt
import time

# 注意：这需要 NVIDIA 显卡 和 大约 4GB+ 显存
# 如果没有显卡，这行代码会报错或者非常慢


def generate_ai_image(config, output_path="ai_output.png"):
    print("正在初始化 AI 模型 (首次运行会下载 4GB 模型，请耐心等待)...")

    # 使用著名的二次元/2.5D 模型 (可以换成 'runwayml/stable-diffusion-v1-5' 走写实风)
    model_id = "dreamlike-art/dreamlike-photoreal-2.0"

    try:
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id, torch_dtype=torch.float16
        )
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipe = pipe.to("cuda")  # 必须有 NVIDIA 显卡

        # 启用一些优化
        # pipe.enable_attention_slicing()

        prompt = build_prompt(config)
        negative_prompt = "low quality, bad anatomy, worst quality, lowres, blurry, pixelated, deformed, ugly, bad hands, extra limbs, cartoon, vector art, flat color"

        print(f"正在生成: {prompt}")

        image = pipe(
            prompt,
            negative_prompt=negative_prompt,
            width=512,
            height=768,
            num_inference_steps=25,
            guidance_scale=7.5,
        ).images[0]

        image.save(output_path)
        print(f"生成完成: {output_path}")
        return output_path

    except Exception as e:
        print(f"AI 生成失败: {e}")
        print("提示: 请确保安装了 pytorch 和 diffusers，并且有 NVIDIA 显卡")
        return None


if __name__ == "__main__":
    # 模拟从前端传来的配置
    test_config = {
        "theme_key": "xianxia",
        "parts": {
            "head": "sage_beard",
            "body": "hanfu_scholar",
            "held": "jian",
            "hair": "topknot",
        },
    }
    generate_ai_image(test_config, "test_ai_xianxia.png")
