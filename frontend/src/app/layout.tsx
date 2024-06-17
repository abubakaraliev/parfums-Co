"use client";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import createStore from "react-auth-kit/createStore";
import AuthProvider from "react-auth-kit/AuthProvider";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

// Configuration for the AuthProvider
const store = createStore({
  authName: "__auth",
  authType: "cookie",
  cookieDomain: "localhost",
  cookieSecure: false,
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  return (
    <AuthProvider store={store}>
        <html>
          <body className={inter.className}>
            <main className="grid h-screen w-full bg-white">{children}</main>
          </body>
        </html>
    </AuthProvider>
  );
}