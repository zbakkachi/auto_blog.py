import os
from google import genai
import requests

# جلب المتغيرات السرية من بيئة GitHub Secrets
WP_URL = os.environ.get("WP_URL")
WP_USER = os.environ.get("WP_USER")
WP_PASS = os.environ.get("WP_PASS")
AI_API_KEY = os.environ.get("AI_API_KEY")


def generate_recipe_with_ai():
    """توليد مقال وصفة طبخ باللغة الإنجليزية وتنسيقه بصيغة HTML"""
    client = genai.Client(api_key=AI_API_KEY)

    prompt = (
        "You are an expert SEO content writer and professional chef. Write a"
        " unique, SEO-optimized food recipe article in English. The output must"
        " be in clean HTML format, including headings (<h2>), a list of"
        " ingredients (<ul>), and step-by-step instructions (<ol>). Format your"
        " exact response in two parts separated strictly by a vertical bar (|):"
        " the first line must be ONLY the article title, and the second part"
        " must be the complete HTML content."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    text_output = response.text.strip()

    if "|" in text_output:
        parts = text_output.split("|", 1)
        title = parts[0].strip()
        content = parts[1].strip()
    else:
        title = "Delicious New Recipe"
        content = text_output

    return title, content


def publish_to_wordpress():
    """إرسال المقال الإنجليزي ونشره مباشرة على ووردبريس"""
    print("جاري توليد المقال باللغة الإنجليزية...")
    title, content = generate_recipe_with_ai()

    payload = {
        "title": title,
        "content": content,
        "status": "publish",  # أو "draft" للمراجعة قبل النشر
    }

    print(f"جاري نشر المقال بعنوان: {title}")
    response = requests.post(WP_URL, json=payload, auth=(WP_USER, WP_PASS))

    if response.status_code == 201:
        print("تم نشر المقال الإنجليزي بنجاح على المدونة!")
    else:
        print(f"فشل النشر، رمز الخطأ: {response.status_code}")
        print(f"التفاصيل: {response.text}")


if __name__ == "__main__":
    publish_to_wordpress()
