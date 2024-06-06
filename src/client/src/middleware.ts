import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico|opengraph-image.png).*)',
  ],
};

const ALLOWED_PATHS = ['/', '/dashboard'];

export function middleware(request: NextRequest) {
  if (!ALLOWED_PATHS.includes(request.nextUrl.pathname)) {
    return NextResponse.redirect(new URL('/', request.url));
  }
  return NextResponse.next();
}
