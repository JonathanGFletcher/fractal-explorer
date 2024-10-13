import requests

if __name__ == "__main__":
    res = requests.post("http://localhost/api/render/video/julia", json={
        "start": {
            "power": 2,
            "constant": {
                "x": -0.8,
                "y": 0.156,
            },
            "center": {
                "x": 0.0,
                "y": 0.0,
            },
            "scale": 1,
            "iterations": 500,
            "samples": 4,
            "dimensions": {
                "width": 1920,
                "height": 1080,
                "view_min_x": 0,
                "view_min_y": 0,
                "view_max_x": 1920,
                "view_max_y": 1080,
            },
            "colors": [],
        },
        "end": {
            "power": 2,
            "constant": {
                "x": -0.8,
                "y": 0.156,
            },
            "center": {
                "x": 0.0,
                "y": 0.0,
            },
            "scale": 131072,
            "iterations": 500,
            "samples": 4,
            "dimensions": {
                "width": 300,
                "height": 200,
                "view_min_x": 0,
                "view_min_y": 0,
                "view_max_x": 299,
                "view_max_y": 199,
            },
            "colors": [],
        },
        "seconds": 60,
    })
    print(res.status_code, res.reason)