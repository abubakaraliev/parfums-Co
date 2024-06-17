import React, { useEffect, useState } from "react";
import { getAllProducts } from "../hooks/useFetchProduct";

export default function DiscoverComponent() {
  const [products, setProducts] = useState<Product[]>([]);
  const authHeader = "";

  useEffect(() => {
    async function fetchProducts() {
      const productData = {};
      const fetchedProducts = await getAllProducts(productData, authHeader);
      setProducts(fetchedProducts);
    }
    fetchProducts();
  }, []);

  return (
    <div className="flex flex-wrap justify-center items-center gap-4 max-w-3xl mx-auto">
      {products.map((product) => (
        <div key={product.id} className="w-full sm:w-1/2 md:w-1/3 lg:w-1/4 p-2">
          <div className="h-full rounded-md overflow-hidden shadow-md hover:shadow-lg flex flex-col">
            <div className="relative">
              <img
                className="w-full h-48 object-cover"
                src={`http://localhost:8000/static/media/${product.image}`}
                alt={product.name}
              />
              {product && (
                <div className="absolute top-0 right-0 bg-red-500 text-white px-2 py-1 m-2 rounded-md text-sm font-medium">
                  SALE
                </div>
              )}
            </div>
            <div className="p-4 flex flex-col flex-grow">
              <h3 className="text-lg text-black font-medium mb-2">
                {product.name}
              </h3>
              <p className="text-gray-600 text-sm mb-4">
                {product.description}
              </p>
              <div className="mt-auto flex flex-col justify-center items-center gap-3">
                <span className="font-bold text-lg text-black">
                  ${product.price.toFixed(2)}
                </span>
                <button className="text-white bg-[#050708] hover:bg-[#050708]/80 py-2 px-4 rounded">
                  Add to cart
                </button>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
