#!/usr/bin/env python3

import os
import sys
from operator import itemgetter, attrgetter


def process_jpegs(directory):
    jpeg_dict = {}
    files = os.listdir(directory)
    jpeg_files = [f for f in files if f.endswith('.jpeg')]
    for jpeg in jpeg_files:
        file_name = os.path.splitext(jpeg)[0]
        (top_glaze, bottom_glaze) = file_name.split('_')
        if top_glaze not in jpeg_dict:
            jpeg_dict[top_glaze] = {'over': [bottom_glaze], 'under':[]}
        else:
            jpeg_dict[top_glaze]['over'].append(bottom_glaze)

        if bottom_glaze not in jpeg_dict:
            jpeg_dict[bottom_glaze] = {'over':[], 'under': [top_glaze]}
        else:
            jpeg_dict[bottom_glaze]['under'].append(top_glaze)

        #ret['top_glaze'] = ret['top_glaze'].replace('-', ' ').title()
        #ret['bottom_glaze'] = ret['bottom_glaze'].replace('-', ' ').title()
    return jpeg_dict


def make_page(glaze, glaze_details):
    # take the top_glaze_lc and open an .html file
    glaze_title = glaze.replace('-', ' ').title()
    with open("pages/{0}.html".format(glaze),'w') as f:

        f.write("""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
""")
        f.write(glaze_title)

        f.write("""\
</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 20px;
        }
        h1 {
            text-align: center;
            margin-bottom: 40px;
        }
        .glaze-row {
            max-width: 1200px;
            margin: 0 auto 40px auto;
        }
        .glaze-row h2 {
            text-align: center;
            background-color: #d3d3d3;
            padding: 10px;
            margin-top: 0;
        }
        .glaze-row ul {
            list-style-type: none;
            padding-left: 0;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
        }
        .glaze-row li {
            margin: 10px;
            list-style: none;
            position: relative;
            text-align: center;
        }
        .glaze-row img {
            max-width: 200px;
            height: auto;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.3s;
        }
        .glaze-row img:hover {
            transform: scale(1.05);
        }
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            padding-top: 60px;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0, 0, 0, 0.9);
        }
        .modal-content {
            margin: auto;
            display: block;
            width: 80%;
            max-width: 700px;
        }
        .modal-content img {
            width: 100%;
            height: auto;
            border-radius: 8px;
        }
        .close {
            position: absolute;
            top: 30px;
            right: 35px;
            color: #ffffff;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>
""")
        f.write(glaze_title)

        f.write("""\
    </h1>
    <div class="glaze-row">
        <h2>Over</h2>
        <ul>
""")

        for over in glaze_details['over']:
            f.write("<li>\n")
            f.write("<img src=\"../glazes/{0}_{1}.jpeg\" alt=\"{0} Over {1}\" onclick=\"enlargeImage(this)\">".format(glaze, over))
            f.write("<p>{0} Over {1}</p>".format(glaze_title, over.replace('-', ' ').title()))        
            f.write("</li>\n")
        f.write("""\
        </ul>
    </div>

    <div class="glaze-row">
        <h2>Under</h2>
        <ul>
""")
        for under in glaze_details['under']:
            f.write("<li>\n")
            f.write("<img src=\"../glazes/{0}_{1}.jpeg\" alt=\"{0} Over {1}\" onclick=\"enlargeImage(this)\">".format(under, glaze))
            f.write("<p>{0} Over {1}</p>".format(under.replace('-', ' ').title(), glaze_title))        
            f.write("</li>\n")
        f.write("""\
        </ul>
    </div>""")

        f.write("""\
    <div id="myModal" class="modal" onclick="closeModal(event)">
        <span class="close" onclick="closeModal(event)">&times;</span>
        <div class="modal-content">
            <img id="modalImg" src="" alt="Enlarged Image">
        </div>
    </div>

    <script>
        function enlargeImage(imgElement) {
            const modal = document.getElementById("myModal");
            const modalImg = document.getElementById("modalImg");
            modal.style.display = "block";
            modalImg.src = imgElement.src;
        }

        function closeModal(event) {
            const modal = document.getElementById("myModal");
            const modalContent = document.querySelector('.modal-content img');

            if (event.target !== modalContent) {
                modal.style.display = "none";
            }
        }
    </script>
</body>
</html>                
""")




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate.py <directory_path>")
    else:
        directory_path = sys.argv[1]
        jpegs = process_jpegs(directory_path)
        for glaze in sorted(jpegs):
            make_page(glaze, jpegs[glaze])
