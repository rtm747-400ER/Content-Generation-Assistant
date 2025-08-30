import os
import requests
import base64
from typing import List
import json

CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
DEFAULT_MODEL = "@cf/stabilityai/stable-diffusion-xl-base-1.0"


class ImageGenerator:
    """
    ImageGenerator for Cloudflare Workers AI (Stable Diffusion XL Base).
    .generate(prompt, width=1024, height=1024) -> List[bytes]
    """

    def __init__(self, model_slug: str = None, timeout: int = 60):
        self.model_slug = model_slug or DEFAULT_MODEL
        self.account_id = CLOUDFLARE_ACCOUNT_ID
        self.token = CLOUDFLARE_API_TOKEN
        self.timeout = timeout

        if not self.token or not self.account_id:
            raise RuntimeError(
                "Missing CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID env vars. "
                "Set them and restart your terminal/VSCode."
            )

        self.url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model_slug}"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def generate(self, prompt: str, width: int = 1024, height: int = 1024, **kwargs) -> List[bytes]:
        """
        Generate image(s) from prompt and return a list of raw image bytes.
        kwargs are forwarded in JSON payload (e.g., guidance_scale, aspect_ratio if supported).
        """
        payload = {"prompt": prompt, "width": width, "height": height, **kwargs}

        try:
            resp = requests.post(self.url, headers=self.headers, json=payload, timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")

        if resp.status_code != 200:
            try:
                err = resp.json()
                raise RuntimeError(f"Cloudflare AI Error {resp.status_code}: {err}")
            except json.JSONDecodeError:
                raise RuntimeError(f"Cloudflare AI Error {resp.status_code}: {resp.text}")

        # Handle direct binary image response
        content_type = resp.headers.get('content-type', '').lower()
        if content_type.startswith('image/') or resp.content.startswith(b'\xff\xd8\xff'):
            return [resp.content]

        # Parse JSON response
        try:
            data = resp.json()
        except json.JSONDecodeError:
            # Fallback for direct binary that doesn't have image content-type
            if b'\xff\xd8\xff' in resp.content[:10] or b'\x89PNG' in resp.content[:10]:
                return [resp.content]
            raise RuntimeError(f"Invalid response format")

        result = data.get("result")
        if result is None:
            if "error" in data:
                raise RuntimeError(f"Cloudflare API Error: {data['error']}")
            raise RuntimeError(f"No 'result' in response: {data}")

        # Extract single image from result
        if not isinstance(result, dict) or "image" not in result:
            raise RuntimeError(f"Expected dict with 'image' key, got: {type(result)}")

        try:
            image_bytes = base64.b64decode(result["image"])
        except Exception as e:
            raise RuntimeError(f"Failed to decode image: {e}")

        return [image_bytes]


# test
if __name__ == "__main__":
    test_prompt = "A simple test prompt: a red apple on a wooden table, photorealistic"
    
    if CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID:
        gen = ImageGenerator()
        try:
            imgs = gen.generate(test_prompt, width=512, height=512)
            print(f"Success! Generated {len(imgs)} images. First image: {len(imgs[0])} bytes")
        except Exception as e:
            print(f"ERROR: {e}")
    else:
        print("Missing environment variables - cannot test")