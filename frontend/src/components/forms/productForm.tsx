"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { CreateProduct } from "@/hooks/useFetchProduct";
import useAuthHeader from "react-auth-kit/hooks/useAuthHeader";
import useIsAuthenticated from "react-auth-kit/hooks/useIsAuthenticated";

const ProductForm = () => {
  const isAuthenticated = useIsAuthenticated();
  const authHeader = useAuthHeader() || "";
  const router = useRouter();

  const [product, setProduct] = useState<{
    category: string;
    name: string;
    slug: string;
    price: string;
    description: string;
    image: File | null;
  }>({
    category: "",
    name: "",
    slug: "",
    price: "",
    description: "",
    image: null,
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setProduct((prevProduct) => ({
      ...prevProduct,
      [name]: value,
    }));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      setProduct((prevProduct) => ({
        ...prevProduct,
        image: file,
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!isAuthenticated) {
      router.push("/login");
      return;
    }

    try {
      const response = await CreateProduct(product, authHeader);
      console.log("Product created:", response);
      router.push("/admin/dashboard/products");
    } catch (error) {
      console.error("Failed to create product:", error);
    }
  };

  return (
    <div className="max-w-md mx-auto">
      <h2 className="text-xl font-semibold mb-4">Add product</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="category" className="block font-medium">
            Category
          </label>
          <input
            type="text"
            id="category"
            name="category"
            value={product.category}
            onChange={handleInputChange}
            className="mt-1 p-2 w-full border-gray-300 rounded-md"
          />
        </div>
        <div>
          <label htmlFor="name" className="block font-medium">
            Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={product.name}
            onChange={handleInputChange}
            className="mt-1 p-2 w-full border-gray-300 rounded-md"
          />
        </div>
        <div>
          <label htmlFor="slug" className="block font-medium">
            Slug
          </label>
          <input
            type="text"
            id="slug"
            name="slug"
            value={product.slug}
            onChange={handleInputChange}
            className="mt-1 p-2 w-full border-gray-300 rounded-md"
          />
        </div>
        <div>
          <label htmlFor="price" className="block font-medium">
            Price
          </label>
          <input
            type="text"
            id="price"
            name="price"
            value={product.price}
            onChange={handleInputChange}
            className="mt-1 p-2 w-full border-gray-300 rounded-md"
          />
        </div>
        <div>
          <label htmlFor="description" className="block font-medium">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={product.description}
            onChange={handleInputChange}
            className="mt-1 p-2 w-full border-gray-300 rounded-md"
          ></textarea>
        </div>
        <div>
          <label htmlFor="image" className="block font-medium">
            Image
          </label>
          <input
            type="file"
            id="image"
            name="image"
            onChange={handleFileChange}
            className="mt-1 w-full border-gray-300 rounded-md"
          />
        </div>
        <button
          type="submit"
          className="bg-blue-500 text-white py-2 px-4 rounded-md"
        >
          Submit
        </button>
      </form>
    </div>
  );
};

export default ProductForm;
