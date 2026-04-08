
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch.nn.functional as F
import numpy as np
import faiss

model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")

#embedding of top1
image1 = Image.open("top.jpg")
inputs1 = processor(images=image1, return_tensors="pt")
embedding1 = model.vision_model(**inputs1).pooler_output

#print(embedding1.shape)

#embedding of top2
image2 = Image.open("top2.jpg")
inputs2 = processor(images=image2, return_tensors="pt")
embedding2 = model.vision_model(**inputs2).pooler_output

#embedding of skirt
image3 = Image.open("skirt.jpg")
inputs3 = processor(images=image3, return_tensors="pt")
embedding3 = model.vision_model(**inputs3).pooler_output

#embedding of top3
image4 = Image.open("top3.jpg")
inputs4 = processor(images=image4, return_tensors="pt")
embedding4 = model.vision_model(**inputs4).pooler_output

#embedding of top5
image5 = Image.open("top5.jpg")
inputs5 = processor(images=image5, return_tensors="pt")
embedding5 = model.vision_model(**inputs5).pooler_output


#calculate similarity between top1 and top2
sim_12 = F.cosine_similarity(embedding1, embedding2)

#calculate similarity between top1 and skirt
sim_13 = F.cosine_similarity(embedding1, embedding3)

#calculate similarity betwen same top
sim_11 = F.cosine_similarity(embedding1, embedding1)

#calculate similarity between top1 and top3
sim_14 = F.cosine_similarity(embedding1, embedding4)

#calculate similarity between top1 and top5
sim_15 = F.cosine_similarity(embedding1, embedding5)

print(f"Similar images score: {sim_12.item():.4f}")
print(f"Different images score: {sim_13.item():.4f}")
print(f"Same top score: {sim_11.item():.4f}")
print(f"Similar images score: {sim_14.item():.4f}")
print(f"Similar images score: {sim_15.item():.4f}")

print(f"Image 1 embedding first 5 values: {embedding1[0][:5]}")
print(f"Image 2 embedding first 5 values: {embedding2[0][:5]}")
print(f"Image 3 embedding first 5 values: {embedding3[0][:5]}")
print(f"Image 4 embedding first 5 values: {embedding4[0][:5]}")
print(f"Image 5 embedding first 5 values: {embedding5[0][:5]}")


# Simulate a small database of 3 listing embeddings
# In reality these would be your sellers' listing images
all_embeddings = np.array([
    embedding1.detach().numpy(),
    embedding2.detach().numpy(),
    embedding3.detach().numpy(),
    embedding4.detach().numpy(),
    embedding5.detach().numpy()
    
]).squeeze()

# Build the FAISS index
index = faiss.IndexFlatIP(768)  # 768 = your embedding size
faiss.normalize_L2(all_embeddings)
index.add(all_embeddings)

# Search using image1 as the query
query = embedding1.detach().numpy()
faiss.normalize_L2(query)
distances, indices = index.search(query, k=3)  # return top 3 matches

print(f"Top matches (indices): {indices}")
print(f"Similarity scores: {distances}")