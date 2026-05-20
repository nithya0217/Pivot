import FeedContainer from "@/components/FeedContainer";
import TopNavbar from "@/components/TopNavbar";

export default function FeedPage() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <TopNavbar />
      <main className="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <FeedContainer />
      </main>
    </div>
  );
}
