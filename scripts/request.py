import requests

if __name__ == "__main__":
    # res = requests.post("http://localhost/api/render/video/julia", json={
    #     "start": {
    #         "power": 2,
    #         "constant": {
    #             "x": -0.8,
    #             "y": 0.156,
    #         },
    #         "center": {
    #             "x": 0.0,
    #             "y": 0.0,
    #         },
    #         "scale": 1,
    #         "iterations": 500,
    #         "samples": 1,
    #         "dimensions": {
    #             "width": 300,
    #             "height": 200,
    #             "view_min_x": 0,
    #             "view_min_y": 0,
    #             "view_max_x": 300,
    #             "view_max_y": 200,
    #         },
    #         "colors": [],
    #     },
    #     "end": {
    #         "power": 2,
    #         "constant": {
    #             "x": -0.8,
    #             "y": 0.156,
    #         },
    #         "center": {
    #             "x": -0.0012809409535713874,
    #             "y": 0.0042718019291621626,
    #         },
    #         "scale": 274877906944,
    #         "iterations": 1000,
    #         "samples": 4,
    #         "dimensions": {
    #             "width": 300,
    #             "height": 200,
    #             "view_min_x": 0,
    #             "view_min_y": 0,
    #             "view_max_x": 299,
    #             "view_max_y": 199,
    #         },
    #         "colors": [],
    #     },
    #     "seconds": 60,
    # })
    # print(res.status_code, res.reason)

    res = requests.get("http://localhost/api/render/video/julia?id=1f38daec-b811-4eae-97e9-46ecb4d98738")
    print(res.json())