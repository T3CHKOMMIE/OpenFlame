import subprocess

import uvicorn
from fastapi import FastAPI
import fbi


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def write_to_screen(image):

    # Path to your image file
    image_path = image
    # Command to display the image using fbi in fullscreen mode
    command = ["sudo", "fbi", "-a", "-T", "1", image_path]

    # Execute the command
    subprocess.run(command)








#startup
if __name__ == "__main__":
    #load base image over HDMI
    write_to_screen("images/progress/OpenFlame2-50.png")
    uvicorn.run(app, host="0.0.0.0", port=8000)