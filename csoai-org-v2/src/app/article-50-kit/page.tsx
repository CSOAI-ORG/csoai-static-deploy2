import type { Metadata } from "next";
import Article50KitClient from "./Article50KitClient";

export const metadata: Metadata = {
  title: "Article 50 Kit",
  description:
    "Everything you need for EU AI Act Article 50 transparency compliance before 2 August 2026. Chatbot disclosure, watermarking, human oversight and documentation.",
  openGraph: {
    title: "CSOAI Article 50 Kit",
    description: "EU AI Act Article 50 compliance toolkit for generative AI systems.",
  },
  alternates: { canonical: "/article-50-kit" },
};

export default function Article50KitPage() {
  return <Article50KitClient />;
}
