import { FC } from 'react';

import cls from './SearchBar.module.scss';

type SearchBarProps = {
    value: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onSubmit?: (e: React.FormEvent) => void;
}

export const SearchBar: FC<SearchBarProps> = ({value, onChange, onSubmit}) => {
	const handleSubmit = (e: React.MouseEvent) => {
		e.preventDefault();
		onSubmit?.(e as unknown as React.FormEvent);
	};

	return (
		<div className={cls.searchBar}>
			<input 
				placeholder='Поиск видео и каналов' 
				className={cls.input} 
				value={value} 
				onChange={onChange}
			/>
            <img 
				src="/icons/search.svg" 
				className={cls.searchIcon} 
				alt="search" 
				onClick={handleSubmit}
			/>
		</div>
	);
};
