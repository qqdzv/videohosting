import { FC } from 'react';
import cls from './BaseInput.module.scss';
import cn from 'classnames';

interface BaseInputProps {
	type: string;
	placeholder: string;
	value: string;
	onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
	onBlur?: () => void;
	disabled?: boolean;
	error?: string;
	label?: string;
	id?: string;
	multiline?: boolean;
	rows?: number;
}

export const BaseInput: FC<BaseInputProps> = ({ 
	type, 
	placeholder, 
	value, 
	onChange, 
	onBlur, 
	disabled, 
	error, 
	label,
	multiline = false,
	rows = 3
}) => {
	return (
		<>
			<div className={cls.inputWrapper}>
				{label && <label className={cls.label}>{label}</label>}
				{multiline ? (
					<textarea
						className={cn(cls.input, cls.textarea)}
						placeholder={placeholder}
						value={value}
						onChange={onChange}
						onBlur={onBlur}
						disabled={disabled}
						rows={rows}
					/>
				) : (
					<input
						className={cls.input}
						type={type}
						placeholder={placeholder}
						value={value}
						onChange={onChange}
						onBlur={onBlur}
						disabled={disabled}
					/>
				)}
			</div>
			{error && <span className={cls.error}>{error}</span>}
		</>
	);
};
