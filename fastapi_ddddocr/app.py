import argparse
import base64
import io
from typing import Annotated

import ddddocr
import yaml
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image

app = FastAPI()
ocr = ddddocr.DdddOcr()
global allowed_auth_tokens
allowed_auth_tokens = []


def read_config(config_path):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def perform_ocr(image, probability, png_fix):
    return ocr.classification(image, png_fix=png_fix, probability=probability)


@app.post("/ocr")
async def ocr_endpoint(
    auth_token: Annotated[str, Form()],
    file: Annotated[UploadFile | None, File()] = None,
    img_b64: Annotated[str | None, Form()] = None,
    probability: Annotated[bool, Form()] = False,
    png_fix: Annotated[bool, Form()] = False,
):
    global allowed_auth_tokens
    if auth_token not in allowed_auth_tokens:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if (file is None and img_b64 is None) or (file is not None and img_b64 is not None):
        raise HTTPException(
            status_code=400,
            detail="Either file or image must be provided, but not both",
        )

    try:
        if file:
            image_data = await file.read()
            img_b64 = Image.open(io.BytesIO(image_data))
        else:
            image_data = base64.b64decode(img_b64)
            img_b64 = Image.open(io.BytesIO(image_data))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image data")

    ocr_result = perform_ocr(img_b64, probability, png_fix)
    if isinstance(ocr_result, str):
        resp = JSONResponse(content={"ocr_result": ocr_result})
    elif isinstance(ocr_result, dict):
        resp = JSONResponse(content=ocr_result)
    else:
        raise HTTPException(status_code=500, detail="Unknown error")
    return resp


def main():
    global allowed_auth_tokens
    import uvicorn

    parser = argparse.ArgumentParser(description="FastAPI OCR Service")
    parser.add_argument(
        "--config", "-c", type=str, required=True, help="Path to the config file"
    )
    args = parser.parse_args()

    config = read_config(args.config)
    allowed_auth_tokens = config["auth_token"]
    host = config.get("host", "127.0.0.1")
    port = config.get("port", 8000)
    allowed_cors = config.get("allowed_cors", ["*"])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_cors,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(app, host=host, port=port)
