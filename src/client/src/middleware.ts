import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico|opengraph-image.png).*)',
  ],
};

export function middleware(request: NextRequest) {
  if (request.url !== '/') {
    return NextResponse.rewrite(new URL('/', request.url));
  }
}
