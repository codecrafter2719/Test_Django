from django.shortcuts import render,redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Disease, UploadedFile
from django.http import JsonResponse


# Add this new view function
def delete_file(request, file_id):
    try:
        file = UploadedFile.objects.get(id=file_id)
        file.file.delete()  # Delete the actual file
        file.delete()  # Delete the database record
        return JsonResponse({
            'status': 'success',
            'message': 'File deleted successfully'
        })
    except UploadedFile.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'File not found'
        }, status=404)

        
def symptom_checker(request):
    # List of diseases with descriptions
    diseases = [
        {"id": 1, "name": "Acne and Rosacea", "description": "Inflammatory skin conditions affecting the face."},
        {"id": 2, "name": "Actinic Keratosis Basal Cell Carcinoma", "description": "Pre-cancerous and cancerous skin lesions."},
        {"id": 3, "name": "Atopic Dermatitis", "description": "Chronic inflammatory skin condition."},
        {"id": 4, "name": "Bullous Disease", "description": "Group of diseases causing fluid-filled blisters."},
        {"id": 5, "name": "Cellulitis Impetigo", "description": "Bacterial skin infections."},
        {"id": 6, "name": "Eczema", "description": "Inflammatory skin condition causing itchy rashes."},
        {"id": 7, "name": "Exanthems and Drug Eruptions", "description": "Skin rashes caused by medications or infections."},
        {"id": 8, "name": "Hair Loss Photos Alopecia", "description": "Various forms of hair loss conditions."},
        {"id": 9, "name": "Herpes HPV and other STDs", "description": "Sexually transmitted infections affecting the skin."},
        {"id": 10, "name": "Light Diseases and Pigmentation", "description": "Conditions affecting skin color and pigmentation."},
        {"id": 11, "name": "Lupus and Connective Tissue diseases", "description": "Autoimmune conditions affecting multiple organs."},
        {"id": 12, "name": "Melanoma Skin Cancer Nevi and Moles", "description": "Skin cancer and related conditions."},
        {"id": 13, "name": "Nail Fungus and other Nail Disease", "description": "Infections and conditions affecting nails."},
        {"id": 14, "name": "Poison Ivy and Contact Dermatitis", "description": "Allergic skin reactions to various substances."},
        {"id": 15, "name": "Psoriasis and Lichen Planus", "description": "Chronic inflammatory skin conditions."},
        {"id": 16, "name": "Scabies Lyme Disease and Bites", "description": "Parasitic and tick-borne conditions."},
        {"id": 17, "name": "Systemic Disease", "description": "Conditions affecting multiple body systems."},
        {"id": 18, "name": "Seborrheic Keratoses", "description": "Common benign skin growths."},
        {"id": 19, "name": "Tinea Ringworm Candidiasis", "description": "Fungal skin infections."},
        {"id": 20, "name": "Urticaria Hives", "description": "Allergic skin reactions causing welts."},
        {"id": 21, "name": "Vascular Tumors", "description": "Abnormal blood vessel growths."},
        {"id": 22, "name": "Vasculitis Photos", "description": "Blood vessel inflammation conditions."},
        {"id": 23, "name": "Warts Molluscum and Viral Infections", "description": "Viral infections affecting the skin."}
    ]
    
    # Handle file upload
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        # Check file size (2MB = 2 * 1024 * 1024 bytes)
        if uploaded_file.size <= 2 * 1024 * 1024:
            # Check file type
            if uploaded_file.content_type in ['image/jpeg', 'image/jpg', 'image/png']:
                file_instance = UploadedFile(
                    file=uploaded_file,
                    file_name=uploaded_file.name
                )
                file_instance.save()
                messages.success(request, 'File uploaded successfully!')
            else:
                messages.error(request, 'Please upload only PNG, JPG, or JPEG files.')
        else:
            messages.error(request, f'File size ({uploaded_file.size / (1024 * 1024):.2f}MB) exceeds 2MB limit.')
    
    # Get recent uploads
    recent_uploads = UploadedFile.objects.order_by('-uploaded_at')[:5]
    
    return render(request, 'guest_access/symptom_checker.html', {
        'diseases': diseases,
        'recent_uploads': recent_uploads
    })

def disease_summary(request):
    # Dictionary mapping disease IDs to their information
    disease_data = {
        "1": {"name": "Acne and Rosacea", "description": "Inflammatory skin conditions affecting the face."},
        "2": {"name": "Actinic Keratosis Basal Cell Carcinoma", "description": "Pre-cancerous and cancerous skin lesions."},
        "3": {"name": "Atopic Dermatitis", "description": "Chronic inflammatory skin condition."},
        "4": {"name": "Bullous Disease", "description": "Group of diseases causing fluid-filled blisters."},
        "5": {"name": "Cellulitis Impetigo", "description": "Bacterial skin infections."},
        "6": {"name": "Eczema", "description": "Inflammatory skin condition causing itchy rashes."},
        "7": {"name": "Exanthems and Drug Eruptions", "description": "Skin rashes caused by medications or infections."},
        "8": {"name": "Hair Loss Photos Alopecia", "description": "Various forms of hair loss conditions."},
        "9": {"name": "Herpes HPV and other STDs", "description": "Sexually transmitted infections affecting the skin."},
        "10": {"name": "Light Diseases and Pigmentation", "description": "Conditions affecting skin color and pigmentation."},
        "11": {"name": "Lupus and Connective Tissue diseases", "description": "Autoimmune conditions affecting multiple organs."},
        "12": {"name": "Melanoma Skin Cancer Nevi and Moles", "description": "Skin cancer and related conditions."},
        "13": {"name": "Nail Fungus and other Nail Disease", "description": "Infections and conditions affecting nails."},
        "14": {"name": "Poison Ivy and Contact Dermatitis", "description": "Allergic skin reactions to various substances."},
        "15": {"name": "Psoriasis and Lichen Planus", "description": "Chronic inflammatory skin conditions."},
        "16": {"name": "Scabies Lyme Disease and Bites", "description": "Parasitic and tick-borne conditions."},
        "17": {"name": "Systemic Disease", "description": "Conditions affecting multiple body systems."},
        "18": {"name": "Seborrheic Keratoses", "description": "Common benign skin growths."},
        "19": {"name": "Tinea Ringworm Candidiasis", "description": "Fungal skin infections."},
        "20": {"name": "Urticaria Hives", "description": "Allergic skin reactions causing welts."},
        "21": {"name": "Vascular Tumors", "description": "Abnormal blood vessel growths."},
        "22": {"name": "Vasculitis Photos", "description": "Blood vessel inflammation conditions."},
        "23": {"name": "Warts Molluscum and Viral Infections", "description": "Viral infections affecting the skin."}
    }
    
    selected_ids = request.GET.getlist('disease_ids')
    selected_diseases = []
    
    for id in selected_ids:
        if id in disease_data:
            disease_info = disease_data[id]
            selected_diseases.append({
                "id": id,
                "name": disease_info["name"],
                "description": disease_info["description"]
            })
    
    return render(request, 'guest_access/summary.html', {
        'selected_diseases': selected_diseases
    })