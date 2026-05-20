"use client";

import { useEffect, useState } from "react";
import ArticleCard, { type Article } from "./ArticleCard";

export default function FeedContainer() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [selectedArticleId, setSelectedArticleId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    const loadArticles = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch("http://localhost:8000/api/articles", {
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error(`Feed request failed: ${response.status}`);
        }

        const data = await response.json();

        if (!Array.isArray(data)) {
          throw new Error("Unexpected feed response shape");
        }

        setArticles(
          data.map((item) => ({
            id: String(item.id ?? item.article_id ?? item.slug ?? item.title ?? "unknown"),
            title: String(item.title ?? "Untitled article"),
            author: String(item.author ?? "Contributor"),
            tags: Array.isArray(item.tags) ? item.tags : [],
            summary: typeof item.summary === "string" ? item.summary : String(item.description ?? ""),
            content: typeof item.content === "string" ? item.content : undefined,
            published_at: typeof item.published_at === "string" ? item.published_at : undefined,
          }))
        );
      } catch (err) {
        if ((err as Error).name !== "AbortError") {
          console.error(err);
          setError("Unable to load your personalized feed. Please try again.");
        }
      } finally {
        setLoading(false);
      }
    };

    void loadArticles();
    return () => controller.abort();
  }, []);

  const handleArticleSelect = (article: Article) => {
    setSelectedArticleId((current) => (current === article.id ? null : article.id));
  };

  return (
    <section className="space-y-8">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="max-w-3xl space-y-3">
          <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Reader Feed</p>
          <h1 className="text-3xl font-semibold text-slate-900 sm:text-4xl">
            Personalized article discovery
          </h1>
          <p className="text-base leading-7 text-slate-600">
            Browse the latest posts, then click any card to send a silent interaction signal to the recommendation engine.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="rounded-3xl border border-dashed border-slate-200 bg-white p-10 text-center text-slate-600 shadow-sm">
          Loading articles…
        </div>
      ) : error ? (
        <div className="rounded-3xl border border-red-200 bg-red-50 p-6 text-red-700 shadow-sm">
          {error}
        </div>
      ) : articles.length === 0 ? (
        <div className="rounded-3xl border border-slate-200 bg-white p-10 text-center text-slate-600 shadow-sm">
          No articles are available yet. Check back soon or create a post from the write page.
        </div>
      ) : (
        <div className="grid gap-6 xl:grid-cols-2">
          {articles.map((article) => (
            <ArticleCard
              key={article.id}
              article={article}
              selected={selectedArticleId === article.id}
              onSelect={handleArticleSelect}
            />
          ))}
        </div>
      )}
    </section>
  );
}
