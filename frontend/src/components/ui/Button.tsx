interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  loading?: boolean;
  variant?: "primary" | "secondary" | "success" | "outline";
  className?: string;
}

export function Button({
  children,
  onClick,
  loading = false,
  variant = "primary",
  className = "",
}: ButtonProps) {
  const variantStyles = {
    primary: "bg-indigo-600 hover:bg-indigo-500 text-white shadow-sm shadow-indigo-500/20",
    secondary: "bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700",
    success: "bg-emerald-600 hover:bg-emerald-500 text-white shadow-sm shadow-emerald-500/20",
    outline: "bg-transparent hover:bg-slate-800 text-slate-300 border border-slate-700",
  };

  return (
    <button
      onClick={onClick}
      disabled={loading}
      className={`disabled:opacity-50 disabled:cursor-not-allowed px-4 py-2 rounded-lg font-medium transition inline-flex items-center justify-center gap-2 text-sm ${variantStyles[variant]} ${className}`}
    >
      {loading ? (
        <>
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Processing...
        </>
      ) : (
        children
      )}
    </button>
  );
}