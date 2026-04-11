import { FC, useState, useRef, useEffect } from 'react';
import cls from './DropdownMenu.module.scss';

interface DropdownMenuItem {
    label: string;
    onClick: () => void;
    danger?: boolean;
}

interface DropdownMenuProps {
    items: DropdownMenuItem[];
}

export const DropdownMenu: FC<DropdownMenuProps> = ({ items }) => {
    const [isOpen, setIsOpen] = useState(false);
    const menuRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    return (
        <div className={cls.dropdownContainer} ref={menuRef}>
            <button 
                className={cls.triggerButton} 
                onClick={(e) => {
                    e.stopPropagation();
                    setIsOpen(!isOpen);
                }}
            >
                <span className={cls.dots}>•••</span>
            </button>
            
            {isOpen && (
                <div className={cls.menu}>
                    {items.map((item, index) => (
                        <button
                            key={index}
                            className={`${cls.menuItem} ${item.danger ? cls.danger : ''}`}
                            onClick={(e) => {
                                e.stopPropagation();
                                item.onClick();
                                setIsOpen(false);
                            }}
                        >
                            {item.label}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}; 