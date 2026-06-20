import type { Metadata } from "next";
import McpPacksClient from "./McpPacksClient";

export const metadata: Metadata = {
  title: "MCP Packs",
  description:
    "Pre-built MCP server packs for EU AI Act compliance, brand & distribution, agentic finance and more. Drop governance into any AI agent stack.",
  openGraph: {
    title: "CSOAI MCP Packs",
    description: "Governance MCP server packs for AI agent ecosystems.",
  },
  alternates: { canonical: "/mcp-packs" },
};

export default function McpPacksPage() {
  return <McpPacksClient />;
}
