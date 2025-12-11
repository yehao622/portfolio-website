import Link from "next/link";

export default function Header() {
    return (
        <header className="bg-white shadow-sm sticky top-0 z-50">
            <nav className="max-w-6xl mx-auto px-4 py-4">
                <div className="flex justify-between items-center">
                    <Link href="/" className="text-xl font-bold text-slate-800 hover:text-slate-600 transition">
                        Howard(Hao) Ye
                    </Link>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex space-x-6">
                        <a href="#about" className="text-slate-600 hover:text-slate-900 transition">
                            About
                        </a>
                        <a href="#projects" className="text-slate-600 hover:text-slate-900 transition">
                            Projects
                        </a>
                        <a href="#contact" className="text-slate-600 hover:text-slate-900 transition">
                            Contact
                        </a>
                    </div>

                    <button className="md:hidden text-slate-600">
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                </div>
            </nav>
        </header>
    );
}