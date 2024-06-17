import axios from "axios";

const registerUser = async (userData: {
  email: string;
  username: string;
  password: string;
}) => {
  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/users/create",
      userData,
    );
    return response;
  } catch (error) {
    console.log("Failed to register user", error);
    throw error;
  }
};

const loginUser = async (userData: { username: string; password: string }) => {
  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/users/login",
      userData,
    );
    return response;
  } catch (error) {
    console.log("Failed to login user", error);
    throw error;
  }
};

// get all users
const getAllUsers = async () => {
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/users/all"
    );
    return response;
  } catch (error) {
    console.log("Failed to get all users", error);
    throw error;
  }
};

export { registerUser, loginUser, getAllUsers };
