import axios from 'axios';
import useAuthHeader from 'react-auth-kit/hooks/useAuthHeader';
import useIsAuthenticated from 'react-auth-kit/hooks/useIsAuthenticated';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function CategoryForm() {
  const [name, setName] = useState('');
  const [slug, setSlug] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const authHeader = useAuthHeader();
  const isAuthenticated = useIsAuthenticated();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const category = { name, slug };

    try {
      const response = await axios.post('http://127.0.0.1:8000/product/category/create', category, {
        headers: {
          Authorization: authHeader,
        },
      });

      if (response.status !== 200) {
        throw new Error('Something went wrong');
      }

      setSuccess('Category created successfully');
    } catch (error) {
      if (axios.isAxiosError(error)) {
        setError(error.response?.data.detail || error.message);
      } else if (error instanceof Error) {
        setError(error.message);
      } else {
        setError('An unexpected error occurred');
      }
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl font-semibold mb-6">Create Category</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700">Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:border-blue-300"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Description</label>
          <textarea
            value={slug}
            onChange={(e) => setSlug(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:border-blue-300"
            required
          />
        </div>
        {error && <p className="text-red-500">{error}</p>}
        {success && <p className="text-green-500">{success}</p>}
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded mt-4"
        >
          Create Category
        </button>
      </form>
    </div>
  );
}