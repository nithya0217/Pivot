import Link from "next/link";

export default function TopNavbar() {
  return (
    <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/95 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <Link href="/feed" className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-900 text-lg font-bold text-white">
            B
          </div>
          <div className="flex flex-col leading-tight">
            <span className="text-lg font-semibold text-slate-900">BlogPivot</span>
            <span className="text-xs text-slate-500">Reader discovery feed</span>
          </div>
        </Link>

        <div className="flex items-center gap-3">
          <Link
            href="/feed"
            className="text-sm font-medium text-slate-700 transition hover:text-slate-900"
          >
            Feed
          </Link>
          <Link
            href="/write"
            className="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-700"
          >
            Write a Post
          </Link>
        </div>
      </div>
    </header>
  );
}
