# wpAPI.py

import requests
from base64 import b64encode
from io import BytesIO
from PIL import Image
from secrets import token_hex

class WordPress:
    def __init__(self, domain, username, password):
        self.domain = domain
        self.username = username
        self.password = password
        self.base_url = f"https://{self.domain}/wp-json/wp/v2"
        self.headers = {
            "Authorization": f"Basic {b64encode(f'{self.username}:{self.password}'.encode()).decode()}",
            "User-Agent": "Python WordPress Publisher/1.0"
        }

    def _get_content_headers(self):
        return {**self.headers, "Content-Type": "application/json"}
    
    def _get_media_headers(self, content_type):
        return {
            **self.headers,
            "Content-Type": content_type,
            "Content-Disposition": f"attachment; filename={token_hex(8)}.png"
        }

    def category(self, content_data):
        """Upload a category to WordPress and return category ID"""
        data = {'name': content_data}

        try:
            responce = requests.post(f"{self.base_url}/categories", 
                    headers=self._get_content_headers(),
                    json=data
                )
            responce.raise_for_status()
            return responce.json()
                
        except requests.exceptions.HTTPError as e:
            print(f"Content upload failed: {e.response.text}")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def upload_image(self, image_url):
        """Upload media to WordPress and return media ID"""
        try:
            # Download and process image
            response = requests.get(image_url)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            img_format = img.format.lower()
            mime_type = f"image/{img_format}" if img_format else "image/png"
            
            # Convert to bytes
            img_bytes = BytesIO()
            img.save(img_bytes, format=img_format)
            img_bytes.seek(0)

            # Upload to WordPress
            media_headers = self._get_media_headers(mime_type)
            media_response = requests.post(
                f"{self.base_url}/media",
                headers=media_headers,
                data=img_bytes.getvalue()
            )
            media_response.raise_for_status()
            
            return media_response.json()

        except Exception as e:
            print(f"Image upload failed: {str(e)}")
            return None

    def publish(self, content_data, content_type="post"):
        """Create posts/pages on WordPress"""
        endpoint = f"{self.base_url}/posts"
        if content_type == "page":
            endpoint = f"{self.base_url}/pages"

        try:
            response = requests.post(
                endpoint,
                headers=self._get_content_headers(),
                json=content_data
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            print(f"Content upload failed: {e.response.text}")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

# Usage example
if __name__ == "__main__":
    # Initialize client
    site = WordPress(
        domain='domain',
        username="admin",
        password='XXXX XXXX XXXX XXXX XXXX XXXX'
    )

