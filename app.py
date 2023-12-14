import base64
import io
from rembg import remove
from PIL import Image
from flask import Flask, jsonify,request,Response, send_file

app = Flask(__name__)

@app.route('/convert_image', methods=['POST'])
def convert_image():
    try:
        image_file = request.files['image']
        
        image_type = image_file.mimetype.split("/")[1]


        processed_image = process_image(image_file,image_type)

        # Convert the processed image to Base64
        base64_image = base64.b64encode(processed_image).decode('utf-8')

        # Create a data structure with the Base64-encoded image
        print(image_type)

        response_data = {'uri': 'data:image/'+ image_type +';base64,' + base64_image}

        # return jsonify(response_data)
        
        # return 'data:image/png;base64,' + base64_image
        return 'data:image/'+ image_type +';base64,' + base64_image

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    

@app.route('/con_image', methods=['POST'])
def con_image():
    image_file = request.files['image']
    image_type = image_file.mimetype.split("/")[1]


    image_uri = convert_image_to_base64(image_file,image_type)
    
    return Response(response=image_uri,status=200,mimetype=f'image/{image_type}')

@app.get("/txt")
def get_txt():
    file_path = 'image.txt'
    
    with open(file_path, 'r') as file:
        file_content = file.read()
    return Response(response=base64.b64decode(file_content),status=200,mimetype="image/png")

def process_image(image_file,image_type: str):
    image = Image.open(image_file)
    output_img = remove(image)
    output_buffer = io.BytesIO()
    print(image_type)
    output_img.save(output_buffer, format=image_type.upper())
        
    processed_image = output_buffer.getvalue()

    return processed_image




def convert_image_to_base64(image_file,image_type: str):
    image = Image.open(image_file)
    output_buffer = io.BytesIO()

    image.save(output_buffer, format=image_type.upper())
    processed_image = output_buffer.getvalue()
    base64_image = base64.b64encode(processed_image).decode('utf-8')
    return base64_image

if __name__ == "__main__":
    app.run(debug=True)