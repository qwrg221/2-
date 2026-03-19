from flask import Blueprint, request, jsonify
from PIL import Image as PILImage
import io
import datetime
from model import db, Image

bp = Blueprint('api', __name__)

@bp.route('/api/image/add', methods=['POST'])
def add_image():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image uploaded'}), 400
    
    filename = file.filename
    image_bytes = file.read()
    
    size = len(image_bytes)
    from PIL import Image as PILImage
    import io
    
    image_stream = io.BytesIO(image_bytes)
    with PILImage.open(image_stream) as img:
        resolution = f"{img.width}x{img.height}"
    
    date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_image = Image(
        filename=filename,
        image_data=image_bytes,
        size=size,
        resolution=resolution,
        date_created=date_created
    )
    db.session.add(new_image)
    db.session.commit()
    
    return jsonify({'message': 'Image saved', 'id': new_image.id})

@bp.route('/api/image/info', methods=['GET'])
def get_image_info():
    image_id = request.args.get('id')
    image = Image.query.get(image_id)
    if not image:
        return jsonify({'error': 'Image not found'}), 404
    
    return jsonify({
        'filename': image.filename,
        'size': image.size,
        'resolution': image.resolution,
        'date_created': image.date_created
    })

@bp.route('/api/image/change/name', methods=['PUT'])
def change_image_name():
    data = request.json
    image_id = data.get('id')
    new_name = data.get('new_name')
    
    image = Image.query.get(image_id)
    if not image:
        return jsonify({'error': 'Image not found'}), 404
    
    image.filename = new_name
    db.session.commit()
    return jsonify({'message': 'Name changed'})

@bp.route('/api/image', methods=['GET'])
def get_all_images():
    images = Image.query.all()
    result = []
    for img in images:
        result.append({
            'id': img.id,
            'filename': img.filename,
            'size': img.size,
            'resolution': img.resolution,
            'date_created': img.date_created
        })
    return jsonify(result)