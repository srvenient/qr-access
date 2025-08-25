'use client';

import React, {useEffect} from "react";
import {useAuthStore} from "@/common/store/auth.store";
import {useRouter} from "next/navigation";

export default function DashboardLayout({children}: Readonly<{
  children: React.ReactNode;
}>) {
  const { isAuthenticated } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace('/sign-in');
    }
  }, [isAuthenticated, router]);

  return (
    <div className="min-h-screen flex flex-col">
      {children}
    </div>
  );
}