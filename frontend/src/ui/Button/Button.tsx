import { FC } from 'react';
import cls from './Button.module.scss';
import cn from 'classnames';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
	text: string;
	onClick: () => void;
	disabled?: boolean;
	primary?: boolean;
	subscribed?: boolean;
	loading?: boolean;
	size?: string;
}

export const Button: FC<ButtonProps> = ({
	text,
	onClick,
	disabled = false,
	primary = false,
	subscribed = false,
	loading = false,
	size = 'm',
	className,
	...props
}) => {
	return (
		<button
			className={cn(
				cls.btn,
				primary && cls.primary,
				subscribed && cls.subscribed,
				loading && cls.loading,
				className,
				cls[size],
			)}
			{...props}
			disabled={disabled || loading}
			onClick={onClick}
		>
			{loading ? <span className={cls.spinner} /> : <span className={cls.inner}>{text}</span>}
		</button>
	);
};
