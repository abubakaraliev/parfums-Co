import axios from "axios";

// create product
interface FormData {
  category: string;
  name: string;
  slug: string;
  price: string;
  description: string;
  image: File | null;
}

const CreateProduct = async (formData: FormData, authHeader: string) => {
  try {
    const data = new FormData();
    data.append("category", formData.category);
    data.append("name", formData.name);
    data.append("slug", formData.slug);
    data.append("price", formData.price);
    data.append("description", formData.description);
    if (formData.image) {
      data.append("image", formData.image);
    }

    const response = await axios.post(
      "http://localhost:8000/product/product/create",
      data,
      {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: authHeader,
        },
      },
    );
    return response.data;
  } catch (error) {
    console.log("Failed to create product", error);
    throw error;
  }
};

const DeleteProduct = async (productId: string, authHeader: string) => {
  try {
    const response = await axios.delete(
      `http://localhost:8000/product/delete/${productId}`,
      {
        headers: {
          Authorization: authHeader,
        },
      },
    );
    return response.data;
  } catch (error) {
    console.log("Failed to delete product", error);
    throw error;
  }
};

interface ProductQuery {
  [key: string]: any;
}
// Get all products
const getAllProducts = async (
  productData: ProductQuery = {},
  authHeader: string,
) => {
  try {
    const response = await axios.get("http://localhost:8000/product/all", {
      params: productData,
      headers: {
        Authorization: authHeader,
      },
    });
    return response.data;
  } catch (error) {
    console.log("Failed to get all products", error);
    throw error;
  }
};

export { getAllProducts, CreateProduct, DeleteProduct };
