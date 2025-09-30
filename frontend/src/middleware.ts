import {NextRequest, NextResponse} from "next/server";

const API_URL = process.env.BACKEND_URL || "http://localhost:8000";

async function isTokenValid(token: string | undefined) {
  if (!token) return false;

  try {
    const res = await fetch(`${API_URL}/auth/validate-token`, {
      headers: {Authorization: `Bearer ${token}`},
    });
    if (!res.ok) return false;

    const data = await res.json();
    return data.valid;
  } catch {
    return false;
  }
}

export async function middleware(req: NextRequest) {
  const token = req.cookies.get('token')?.value;
  const pathname = req.nextUrl.pathname.replace(/\/$/, '');

  if (pathname.startsWith('/dashboard')) {
    const valid = await isTokenValid(token);
    if (!valid) {
      return NextResponse.redirect(new URL('/sign-in', req.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};
