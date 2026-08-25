export function Button({ children, onClick, loading = false }: { children: React.ReactNode; onClick?: () => void; loading?: boolean }) {
  return (
    <button
      onClick={onClick}
      disabled={loading}
      className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white px-4 py-2 rounded-lg font-medium transition"
    >
      {loading ? "Running..." : children}
    </button>
  );
}