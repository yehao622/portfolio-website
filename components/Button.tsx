import Link from "next/link";

interface ButtonProps {
    href?: string;
    onClick?: () => void;
    variant?: 'primary' | 'secondary';
    children: React.ReactNode;
    className?: string;
}

export default function Button({
    href,
    onClick,
    variant = 'primary',
    children,
    className = ''
}: ButtonProps) {
    const baseStyles = "px-6 py-3 rounded-lg font-medium transition";
    const variantStyles = {
        primary: "bg-blue-600 text-white hover:bg-blue-700",
        secondary: "bg-slate-200 text-slate-800 hover:bg-slate-300"
    };

    const combineStyles = `${baseStyles} ${variantStyles[variant]} ${className}`;

    // If href is provided, render as Link
    if (href) {
        return (
            <Link href={href} className={combineStyles}>
                {children}
            </Link>
        );
    }

    return (
        <button onClick={onClick} className={combineStyles}>
            {children}
        </button>
    );
}