"use client";
import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import useAuthHeader from "react-auth-kit/hooks/useAuthHeader";
import useIsAuthenticated from "react-auth-kit/hooks/useIsAuthenticated";
import { getAllProducts, DeleteProduct } from "../hooks/useFetchProduct";
import SpinnerComponent from "../components/spinnerComponent";
import ModalComponent from "../components/modalComponent";
import productUpdateModal from "./forms/productUpdateModal";

export default function Products() {
  const [data, setData] = useState<any[]>([]);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [selectedProductId, setSelectedProductId] = useState<string>("");
  const router = useRouter();

  const authHeader: string = useAuthHeader() || "";

  const isAuthenticated = useIsAuthenticated();

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
    } else {
      const fetchData = async () => {
        try {
          const response = await getAllProducts({}, authHeader);
          setData(response);
          setLoading(false);
        } catch (error) {
          setError(
            error instanceof Error
              ? error
              : new Error("An unknown error occurred"),
          );
          setLoading(false);
        }
      };

      fetchData();
    }
  }, [authHeader, isAuthenticated, mounted]);

  const handleAddProduct = () => {
    router.push("/admin/dashboard/products/createProduct");
  };

  const handleDeleteProduct = (productId: string) => {
    setSelectedProductId(productId);
    setModalOpen(true);
  };

  const confirmDeleteProduct = async (productId: string) => {
    try {
      await DeleteProduct(productId, authHeader);
      setData(data.filter((product) => product.id !== productId));
      setModalOpen(false);
    } catch (error: unknown) {
      console.error("Failed to delete product", error);
      setModalOpen(false);
    }
  };

  if (!mounted) {
    return <SpinnerComponent />;;
  }

  if (!isAuthenticated) {
    return <h1>Please login to view products.</h1>;
  }

  if (loading) {
    return <SpinnerComponent />;
  }

  if (error) {
    return <h1>Error: {error.message}</h1>;
  }

  return (
    <div className="container mx-auto px-4 sm:px-8 max-w-3xl">
      <div className="py-8">
        <div className="flex justify-between">
          <h2 className="text-2xl font-semibold leading-tight">Products</h2>
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded"
            onClick={handleAddProduct}
          >
            Add product
          </button>
        </div>
        <div className="mt-4">
          <p className="text-sm text-gray-600">A list of products.</p>
        </div>
        <div className="mt-4">
          <div className="inline-block min-w-full shadow rounded-lg overflow-hidden">
            <table className="min-w-full leading-normal">
              <thead>
                <tr>
                  <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                    Description
                  </th>
                  <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                    Price
                  </th>
                  <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                    Image
                  </th>
                  <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                    Category
                  </th>
                  <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                    Edit
                  </th>
                  <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                    Delete
                  </th>
                </tr>
              </thead>
              <tbody>
                {data.map((product) => (
                  <tr key={product.id}>
                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                      <div className="flex items-center">
                        <div className="ml-3">
                          <p className="text-gray-900 whitespace-no-wrap">
                            {product.name}
                          </p>
                        </div>
                      </div>
                    </td>
                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                      <p className="text-gray-900 whitespace-no-wrap">
                        {product.description}
                      </p>
                    </td>
                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                      <p className="text-gray-900 whitespace-no-wrap">
                        {product.price}
                      </p>
                    </td>
                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                      {product.image && (
                        <img
                          src={`http://localhost:8000/static/media/${product.image}`}
                          alt={product.name}
                          className="w-16 h-16 object-cover"
                        />
                      )}
                    </td>
                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                      <p className="text-gray-900 whitespace-no-wrap">
                        {product.category}
                      </p>
                    </td>
                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                      <button className="text-blue-600 hover:text-blue-900">
                        Edit
                      </button>
                    </td>
                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                      <button
                        className="text-red-600 hover:text-red-900"
                        onClick={() => handleDeleteProduct(product.id)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <ModalComponent
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        onDelete={() => confirmDeleteProduct(selectedProductId)}
        productId={selectedProductId}
      />
    </div>
  );
}
