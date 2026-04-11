import { FC, useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { BaseInput } from '@/ui/BaseInput/BaseInput.tsx';
import { Button } from '@/ui/Button/Button';
import cls from './Reg.module.scss';
import fields from './RegSteps.ts';
import { FieldKey } from './RegSteps.ts';
import { Header } from '@/components/Header/Header.tsx';
import { useGetProfileQuery, useRegisterMutation } from '@/store/api/auth.api.ts';
import { IRegisterRequest, ValidationErrors } from '@/types/auth.types';
import { validateEmail, validatePassword, validateRequired } from '@/utils/validation';
import { useAppDispatch, useAppSelector } from '@/hooks/storeHooks.ts';
import { actions } from '@/store/auth/auth.slice.ts';

export const Reg: FC = () => {
	const navigate = useNavigate();
	const dispatch = useAppDispatch();
	const isAuthenticated = useAppSelector((state) => state.auth.isAuthenticated);
	const [register, { isLoading, isSuccess }] = useRegisterMutation();
	const { data: profile, isError: profileError, error: profileErrorData } = useGetProfileQuery(undefined, { skip: !isSuccess });
	const [form, setForm] = useState<IRegisterRequest>({
		username: '',
		email: '',
		password: '',
		first_name: '',
		last_name: ''
	});

	const [errors, setErrors] = useState<ValidationErrors>({});
	const [submitAttempted, setSubmitAttempted] = useState(false);
	const [generalError, setGeneralError] = useState<string | null>(null);
	useEffect(() => {
		if (profile && isSuccess) {
			console.log('Setting user in store:', profile);
			dispatch(actions.setUser(profile));
			navigate('/');
		}
	}, [profile, isSuccess, dispatch, navigate, profileError]);

	const validateForm = (): boolean => {
		const newErrors: ValidationErrors = {};

		// Validate required fields
		Object.keys(form).forEach((key) => {
			const value = form[key as keyof IRegisterRequest];
			const error = validateRequired(value);
			if (error) {
				newErrors[key as keyof IRegisterRequest] = error;
			}
		});

		// Email validation
		if (!newErrors.email) {
			const emailError = validateEmail(form.email);
			if (emailError) newErrors.email = emailError;
		}

		// Password validation
		if (!newErrors.password) {
			const passwordError = validatePassword(form.password);
			if (passwordError) newErrors.password = passwordError;
		}

		setErrors(newErrors);
		return Object.keys(newErrors).length === 0;
	};

	const handleChange = (key: FieldKey, value: string) => {
		setForm((prev) => ({ ...prev, [key]: value }));
		if (submitAttempted) {
			setErrors((prev) => {
				const newErrors = { ...prev };
				delete newErrors[key];
				return newErrors;
			});
		}
		setGeneralError(null);
	};

	const handleSubmit = async () => {
		setSubmitAttempted(true);
		setGeneralError(null);

		if (!validateForm()) {
			return;
		}

		try {
			await register(form).unwrap();
			dispatch(actions.setCredentials());
		} catch (err: any) {
			if (err.data && typeof err.data === 'object') {
				const serverErrors: ValidationErrors = {};
				Object.entries(err.data).forEach(([key, value]) => {
					if (Array.isArray(value)) {
						serverErrors[key as keyof IRegisterRequest] = value[0];
					} else if (typeof value === 'string') {
						serverErrors[key as keyof IRegisterRequest] = value;
					}
				});
				setErrors(serverErrors);
			} else {
				setGeneralError(typeof err.data === 'string' ? err.data : 'Произошла ошибка при регистрации');
			}
		}
	};

	const getFieldError = (key: FieldKey): string | undefined => {
		return errors[key];
	};

	return (
		<main className={cls.reg}>
			<Header />
			<section className={cls.regModal}>
				<h1 className={cls.title}>Регистрация</h1>
				{fields.map(({ key, ...rest }, index) => (
					<BaseInput
						key={index}
						value={form[key]}
						onChange={(e) => handleChange(key, e.target.value)}
						error={getFieldError(key)}
						disabled={isLoading}
						{...rest}
					/>
				))}
				<Button
					text={isLoading ? 'Регистрация...' : 'Зарегистрироваться'}
					onClick={handleSubmit}
					primary
					disabled={isLoading}
					style={{ marginTop: '14px' }}
				/>
				{generalError && <div className={cls.error}>{generalError}</div>}
			</section>
			<nav className={cls.nav}>
				<Link to="/auth/login" className={cls.link}>
					Уже есть аккаунт? Войти
				</Link>
			</nav>
		</main>
	);
};
