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
    ImageGenerator for Cloudflare Workers AI (Stable Diffusion XL Lightning).
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

        # endpoint to call the model
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
        payload = {
            "prompt": prompt,
            "width": width,
            "height": height,
        }
        payload.update(kwargs)

        print(f"Making request to: {self.url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            resp = requests.post(self.url, headers=self.headers, json=payload, timeout=self.timeout)
            
            print(f"Response status: {resp.status_code}")
            print(f"Response headers: {dict(resp.headers)}")
            print(f"Raw response content: {resp.text[:500]}...")  # First 500 chars
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")

        if resp.status_code != 200:
            # Enhanced error handling
            try:
                err = resp.json()
                error_msg = f"Cloudflare AI Error {resp.status_code}: {err}"
            except json.JSONDecodeError:
                error_msg = f"Cloudflare AI Error {resp.status_code}: {resp.text}"
            except Exception:
                error_msg = f"Cloudflare AI Error {resp.status_code}: Unknown error"
            raise RuntimeError(error_msg)

        # Check if response is empty
        if not resp.content:
            raise RuntimeError("Empty response from Cloudflare API")

        # Check if response is binary (direct image) or JSON
        content_type = resp.headers.get('content-type', '').lower()
        print(f"Content-Type: {content_type}")
        
        # If it's an image directly, return it
        if content_type.startswith('image/') or resp.content.startswith(b'\xff\xd8\xff'):  # JPEG magic bytes
            print("Received direct binary image response")
            return [resp.content]
        
        # Otherwise, try to parse as JSON
        try:
            data = resp.json()
        except json.JSONDecodeError as e:
            # If it's not JSON but looks like binary data, treat it as direct image
            if b'\xff\xd8\xff' in resp.content[:10] or b'\x89PNG' in resp.content[:10]:
                print("Response appears to be direct binary image data")
                return [resp.content]
            raise RuntimeError(f"Invalid JSON response from Cloudflare: {e}. Response text: {resp.text[:200]}")

        # Log the structure for debugging
        print(f"Parsed JSON structure: {json.dumps(data, indent=2) if len(str(data)) < 1000 else 'Large response'}")

        # expected shapes:
        # data = {"result": {"image": "<base64>"}}
        # or data = {"result": {"images": ["<base64>", ...]}}
        # or data = {"result": [{"image": "<base64>"}, ...]}
        results: List[bytes] = []

        result = data.get("result")

        if result is None:
            # Check for common error patterns
            if "error" in data:
                raise RuntimeError(f"Cloudflare API Error: {data['error']}")
            if "errors" in data and data["errors"]:
                raise RuntimeError(f"Cloudflare API Errors: {data['errors']}")
            raise RuntimeError(f"Unexpected Cloudflare response (no 'result'): {data}")

        # Case: result is dict with "image" (single)
        if isinstance(result, dict):
            if "image" in result and isinstance(result["image"], str):
                try:
                    results.append(base64.b64decode(result["image"]))
                except Exception as e:
                    raise RuntimeError(f"Failed to decode image base64: {e}")
            # Case: dict with "images" list
            elif "images" in result and isinstance(result["images"], list):
                for img_b64 in result["images"]:
                    if isinstance(img_b64, str):
                        try:
                            results.append(base64.b64decode(img_b64))
                        except Exception as e:
                            raise RuntimeError(f"Failed to decode image base64: {e}")
            else:
                # Log what we actually got
                print(f"Unexpected result structure: {result}")
                raise RuntimeError(f"No 'image' or 'images' key found in result: {list(result.keys())}")
                
        # Case: result is list of dicts
        elif isinstance(result, list):
            for item in result:
                if isinstance(item, dict) and "image" in item and isinstance(item["image"], str):
                    try:
                        results.append(base64.b64decode(item["image"]))
                    except Exception as e:
                        raise RuntimeError(f"Failed to decode image base64: {e}")
                elif isinstance(item, str):
                    # if they returned a base64 string in a list
                    try:
                        results.append(base64.b64decode(item))
                    except Exception as e:
                        raise RuntimeError(f"Failed to decode image base64: {e}")
        else:
            raise RuntimeError(f"Unexpected result type: {type(result)}, value: {result}")

        # If still empty, attempt common keys fallback
        if not results:
            # sometimes image data may be direct string under top-level keys
            # try top-level 'image' or 'images'
            if isinstance(data.get("image"), str):
                try:
                    results.append(base64.b64decode(data.get("image")))
                except Exception as e:
                    raise RuntimeError(f"Failed to decode image base64: {e}")
            elif isinstance(data.get("images"), list):
                for img_b64 in data.get("images"):
                    try:
                        results.append(base64.b64decode(img_b64))
                    except Exception as e:
                        raise RuntimeError(f"Failed to decode image base64: {e}")

        if not results:
            raise RuntimeError(f"No images found in Cloudflare response. Full response: {data}")

        return results


# quick debug helper
if __name__ == "__main__":
    # quick local test (only run from terminal)
    test_prompt = "A simple test prompt: a red apple on a wooden table, photorealistic"
    print("Token present:", bool(CLOUDFLARE_API_TOKEN))
    print("Account ID present:", bool(CLOUDFLARE_ACCOUNT_ID))
    
    if CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID:
        gen = ImageGenerator()
        try:
            imgs = gen.generate(test_prompt, width=512, height=512)
            print("Got", len(imgs), "images. First image size bytes:", len(imgs[0]))
        except Exception as e:
            print("ERROR:", e)
    else:
        print("Missing environment variables - cannot test")