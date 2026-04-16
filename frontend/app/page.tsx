"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

interface Track {
  id: string | null;
  title: string;
  artist: string;
  description: string;
}

export default function Home() {
  const [view, setView] = useState<"search" | "add">("search");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Track[]>([]);
  const [searching, setSearching] = useState(false);

  const [title, setTitle] = useState("");
  const [artist, setArtist] = useState("");
  const [description, setDescription] = useState("");
  const [adding, setAdding] = useState(false);
  const [addSuccess, setAddSuccess] = useState(false);

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;
    setSearching(true);
    setResults([]);
    try {
      const res = await fetch(`${API_URL}/track/query?q=${encodeURIComponent(query.trim())}`);
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error("Search failed:", err);
    } finally {
      setSearching(false);
    }
  }

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim() || !artist.trim() || !description.trim()) return;
    setAdding(true);
    setAddSuccess(false);
    try {
      const res = await fetch(`${API_URL}/track`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: title.trim(), artist: artist.trim(), description: description.trim() }),
      });
      if (res.ok) {
        setAddSuccess(true);
        setTitle("");
        setArtist("");
        setDescription("");
      }
    } catch (err) {
      console.error("Add failed:", err);
    } finally {
      setAdding(false);
    }
  }

  return (
    <div className="flex flex-col items-center min-h-screen px-4 py-16">
      <h1 className="text-4xl font-bold tracking-tight mb-2">Semantic Music Search</h1>
      <p className="text-zinc-400 mb-10">Find tracks by meaning, not just keywords</p>

      {/* Tab switcher */}
      <div className="flex gap-1 bg-zinc-900 rounded-lg p-1 mb-10">
        <button
          onClick={() => setView("search")}
          className={`px-5 py-2 rounded-md text-sm font-medium transition-colors ${
            view === "search" ? "bg-zinc-700 text-white" : "text-zinc-400 hover:text-zinc-200"
          }`}
        >
          Search
        </button>
        <button
          onClick={() => setView("add")}
          className={`px-5 py-2 rounded-md text-sm font-medium transition-colors ${
            view === "add" ? "bg-zinc-700 text-white" : "text-zinc-400 hover:text-zinc-200"
          }`}
        >
          Add Track
        </button>
      </div>

      <div className="w-full max-w-xl">
        {/* Search view */}
        {view === "search" && (
          <>
            <form onSubmit={handleSearch} className="flex gap-2 mb-8">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g. upbeat summer vibes with guitar"
                className="flex-1 bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-sm text-white placeholder-zinc-500 focus:outline-none focus:border-zinc-600 transition-colors"
              />
              <button
                type="submit"
                disabled={searching}
                className="bg-white text-black px-5 py-3 rounded-lg text-sm font-medium hover:bg-zinc-200 transition-colors disabled:opacity-50"
              >
                {searching ? "..." : "Search"}
              </button>
            </form>

            {results.length > 0 && (
              <div className="flex flex-col gap-3">
                {results.map((track, i) => (
                  <div
                    key={track.id ?? i}
                    className="bg-zinc-900 border border-zinc-800 rounded-lg p-4 hover:border-zinc-700 transition-colors"
                  >
                    <div className="flex items-baseline justify-between mb-1">
                      <span className="text-xs text-zinc-500 font-mono">#{i + 1}</span>
                    </div>
                    <h3 className="text-lg font-semibold">{track.title}</h3>
                    <p className="text-sm text-zinc-400 mb-2">{track.artist}</p>
                    <p className="text-sm text-zinc-500 leading-relaxed">{track.description}</p>
                  </div>
                ))}
              </div>
            )}

            {searching && (
              <p className="text-center text-zinc-500 text-sm">Searching...</p>
            )}

            {!searching && results.length === 0 && query && (
              <p className="text-center text-zinc-500 text-sm">No results yet. Try a search above.</p>
            )}
          </>
        )}

        {/* Add track view */}
        {view === "add" && (
          <form onSubmit={handleAdd} className="flex flex-col gap-4">
            <div>
              <label className="block text-sm text-zinc-400 mb-1">Title</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-sm text-white placeholder-zinc-500 focus:outline-none focus:border-zinc-600 transition-colors"
                placeholder="Track title"
              />
            </div>
            <div>
              <label className="block text-sm text-zinc-400 mb-1">Artist</label>
              <input
                type="text"
                value={artist}
                onChange={(e) => setArtist(e.target.value)}
                className="w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-sm text-white placeholder-zinc-500 focus:outline-none focus:border-zinc-600 transition-colors"
                placeholder="Artist name"
              />
            </div>
            <div>
              <label className="block text-sm text-zinc-400 mb-1">Description</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
                className="w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-sm text-white placeholder-zinc-500 focus:outline-none focus:border-zinc-600 transition-colors resize-none"
                placeholder="Describe the track's mood, genre, instruments..."
              />
            </div>
            <button
              type="submit"
              disabled={adding}
              className="bg-white text-black px-5 py-3 rounded-lg text-sm font-medium hover:bg-zinc-200 transition-colors disabled:opacity-50"
            >
              {adding ? "Adding..." : "Add Track"}
            </button>
            {addSuccess && (
              <p className="text-green-400 text-sm text-center">Track added successfully!</p>
            )}
          </form>
        )}
      </div>
    </div>
  );
}
