"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const councilLinks = [
  { href: "/council", label: "Overview" },
  { href: "/council/dome", label: "Dome" },
  { href: "/council/maps", label: "Maps" },
  { href: "/council/compliance", label: "Compliance" },
  { href: "/council/law", label: "Law" },
  { href: "/council/sigil", label: "Sigil" },
];

export default function CouncilNav() {
  const pathname = usePathname();
  return (
    <nav className="border-b border-white/5 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 text-white font-bold tracking-tight">
          <span className="text-emerald-400 text-xl">CSOAI</span>
          <span className="text-slate-500 text-xs uppercase tracking-widest hidden sm:inline">Council</span>
        </Link>
        <div className="flex items-center gap-1 text-sm">
          {councilLinks.map((l) => {
            const active = pathname === l.href;
            return (
              <Link
                key={l.href}
                href={l.href}
                className={`px-3 py-1.5 rounded-lg transition ${
                  active
                    ? "bg-emerald-500/20 text-emerald-300"
                    : "text-slate-400 hover:text-white hover:bg-white/5"
                }`}
              >
                {l.label}
              </Link>
            );
          })}
          <a
            href="https://app.csoai.org/opengridworks"
            target="_blank"
            rel="noopener noreferrer"
            className="px-3 py-1.5 rounded-lg transition text-emerald-400 hover:text-emerald-300 hover:bg-emerald-500/10"
          >
            Atlas →
          </a>
          <a
            href="https://app.csoai.org/opengridworks"
            target="_blank"
            rel="noopener noreferrer"
            className="px-3 py-1.5 rounded-lg transition text-emerald-400 hover:text-emerald-300 hover:bg-emerald-500/10"
          >
            Atlas →
          </a>
          <a
            href="https://councilof.ai"
            target="_blank"
            rel="noopener noreferrer"
            className="px-3 py-1.5 rounded-lg transition text-emerald-400 hover:text-emerald-300 hover:bg-emerald-500/10"
          >
            Run a Council →
          </a>
        </div>
      </div>
    </nav>
  );
}
