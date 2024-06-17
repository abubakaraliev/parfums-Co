import useAuthHeader from "react-auth-kit/hooks/useAuthHeader";
import useIsAuthenticated from "react-auth-kit/hooks/useIsAuthenticated";
import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { parseISO, formatDistanceToNow } from 'date-fns';

interface User {
  username: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export default function MyAccountPage() {
  const isAuthenticated = useIsAuthenticated();
  const authHeader = useAuthHeader();
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
    if (!isAuthenticated) {
      router.push("/login");
    } else {
      axios
        .get("http://127.0.0.1:8000/users/me", {
          headers: {
            Authorization: authHeader,
          },
        })
        .then((response) => {
          setUser(response.data);
        })
        .catch((error) => {
          setError(error.message);
        });
    }
  }, [isAuthenticated, authHeader, router]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setUser((prevState) => prevState ? { ...prevState, [name]: value } : null);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (user) {
      try {
        const response = await axios.put(
          "http://127.0.0.1:8000/users/me",
          { username: user.username, email: user.email },
          {
            headers: {
              Authorization: authHeader,
            },
          }
        );

        if (response.status === 200) {
          console.log("User information updated successfully", response);
        }
      } catch (error) {
        console.error("Failed to update user information:", error);
      }
    }
  };

  const formatRelativeTime = (dateString: string) => {
    const date = parseISO(dateString);
    return formatDistanceToNow(date, { addSuffix: true });
  };

  return (
    <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8 bg-white">
      <div className="px-4 sm:px-0">
        <h3 className="text-base font-semibold leading-7 text-gray-900">
          My Account Information
        </h3>
        <p className="mt-1 max-w-2xl text-sm leading-6 text-gray-500">
          Personal details.
        </p>
      </div>
      {error && <div className="text-red-500">{error}</div>}
      {!user ? (
        <div>Loading...</div>
      ) : (
        <div className="mt-6 border-t border-gray-100">
          <dl className="divide-y divide-gray-100">
            <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
              <dt className="text-sm font-medium leading-6 text-gray-900">
                Username
              </dt>
              <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                {user.username}
              </dd>
            </div>
            <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
              <dt className="text-sm font-medium leading-6 text-gray-900">
                Email address
              </dt>
              <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                {user.email}
              </dd>
            </div>
            <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
              <dt className="text-sm font-medium leading-6 text-gray-900">
                Account created in
              </dt>
              <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                {formatRelativeTime(user.created_at)}
              </dd>
              <dt className="text-sm font-medium leading-6 text-gray-900">
                Account updated at
              </dt>
              <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                {formatRelativeTime(user.updated_at)}
              </dd>
            </div>
          </dl>
          <form onSubmit={handleSubmit} className="mt-8 max-w-3xl space-y-6">
            <div className="sm:col-span-4">
              <label
                htmlFor="email"
                className="block text-sm font-medium leading-6 text-gray-900"
              >
                Email address
              </label>
              <div className="mt-2">
                <input
                  type="email"
                  name="email"
                  id="email"
                  value={user.email || ''}
                  onChange={handleChange}
                  autoComplete="email"
                  className="px-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>
            <div className="sm:col-span-3">
              <label
                htmlFor="username"
                className="block text-sm font-medium leading-6 text-gray-900"
              >
                Username
              </label>
              <div className="mt-2">
                <input
                  type="text"
                  name="username"
                  id="username"
                  value={user.username || ''}
                  onChange={handleChange}
                  autoComplete="username"
                  className="px-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>
            <div className="sm:col-span-6">
              <button
                type="submit"
                className="mt-2 w-full rounded-md bg-indigo-600 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Update Information
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}