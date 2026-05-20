"use client";

import { useState } from "react";

export type Article = {
  id: string;
  title: string;
  author: string;
  tags: string[];
  summary?: string;
  content?: string;
  published_at?: string;
};

type ArticleCardProps = {
  article: Article;
  selected?: boolean;
  onSelect: (article: Article) => void;
};

export default function ArticleCard({
  article,
  selected = false,
  onSelect,
}: ArticleCardProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleClick = async () => {
    if (isSubmitting) {
      return;
    }

    setIsSubmitting(true);

    try {
      await fetch("http://localhost:8000/api/interactions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          article_id: article.id,
          interaction_type: "click",
        }),
      });
    } catch (error) {
      console.error("Unable to send click interaction", error);
    } finally {
      setIsSubmitting(false);
      onSelect(article);
    }
  };

  return (
    <button
      type="button"
      onClick={handleClick}
      className="group w-full rounded-3xl border border-slate-200 bg-white p-6 text-left shadow-sm transition hover:-translate-y-0.5 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-slate-400"
    >
      <div className="flex flex-col gap-4">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-sm font-medium uppercase tracking-[0.18em] text-slate-500">
              {article.author || "Unknown author"}
            </p>
            <h3 className="mt-3 text-xl font-semibold text-slate-900">{article.title}</h3>
          </div>
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-slate-700">
            Click
          </span>
        </div>

        <p className="min-h-[3rem] text-sm leading-6 text-slate-600">
          {article.summary ?? article.content ?? "Tap to reveal the full post preview."}
        </p>

        <div className="flex flex-wrap gap-2">
          {(article.tags ?? []).map((tag) => (
            <span
              key={tag}
              className="inline-flex rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600"
            >
              {tag}
            </span>
          ))}
        </div>

        {selected ? (
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4 text-sm leading-6 text-slate-700">
            <p className="mb-3 text-sm font-semibold text-slate-900">Expanded post preview</p>
            <p>{article.content ?? article.summary ?? "No additional preview available."}</p>
          </div>
        ) : null}

        {isSubmitting ? (
          <p className="text-sm text-slate-500">Recording your click...</p>
        ) : null}
      </div>
    </button>
  );
}
