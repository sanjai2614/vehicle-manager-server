import cloudinary.uploader


def upload_driver_avatar(image):

    result = cloudinary.uploader.upload(
        image,
        folder="vehicle_management/drivers",
        resource_type="image"
    )

    return {
        "url": result["secure_url"],
        "public_id": result["public_id"]
    }


def delete_driver_avatar(public_id):

    if public_id:
        cloudinary.uploader.destroy(public_id)