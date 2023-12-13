import base64
import io
from rembg import remove
from PIL import Image
from flask import Flask, jsonify,request

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
    
    

def process_image(image_file,image_type: str):
    image = Image.open(image_file)
    output_img = remove(image)
    output_buffer = io.BytesIO()
    print(image_type)
    output_img.save(output_buffer, format=image_type.upper())
        
    processed_image = output_buffer.getvalue()

    return processed_image



def process_imagew(image_file,image_type: str):
    
    # input_img = Image.open(image_file)
    # output_img = remove(input_img)
    # output_img.save("bg.png")
    
    # Example: Resize the image to 100x100 pixels
    image = Image.open(image_file)
    # resized_image = image.resize((100, 100))

    # Convert the image to bytes
    output_buffer = io.BytesIO()
    print(image_type)
    image.save(output_buffer, format=image_type.upper())
    # image.save(output_buffer, format='PNG')
    
    # resized_image.save(output_buffer, format='PNG')
    processed_image = output_buffer.getvalue()

    return processed_image

if __name__ == "__main__":
    app.run(debug=True)