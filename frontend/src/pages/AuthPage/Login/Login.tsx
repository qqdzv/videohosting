import { FC, useEffect, useState } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import { BaseInput } from '@/ui/BaseInput/BaseInput.tsx';
import { Button } from '@/ui/Button/Button';
import cls from './Login.module.scss';
import fields from './LoginSteps.ts';
import { FieldKey } from './LoginSteps.ts';
import { Header } from '@/components/Header/Header.tsx';
import { useGetProfileQuery, useLoginMutation } from '@/store/api/auth.api.ts';
import { ILoginRequest, ValidationErrors } from '@/types/auth.types';
import { validateEmail, validateRequired } from '@/utils/validation';
import { useAppDispatch, useAppSelector } from '@/hooks/storeHooks.ts';
import { actions } from '@/store/auth/auth.slice.ts';

export const Login: FC = () => {
	const navigate = useNavigate();
	const dispatch = useAppDispatch();
	const isAuthenticated = useAppSelector((state) => state.auth.isAuthenticated);
	const [login, { isLoading, isSuccess }] = useLoginMutation();
	const { data: profile, isError: profileError, error: profileErrorData } = useGetProfileQuery(undefined, { skip: !isSuccess });
	const [form, setForm] = useState<ILoginRequest>({
		email: '',
		password: ''
	});

	const [errors, setErrors] = useState<ValidationErrors>({});
	const [submitAttempted, setSubmitAttempted] = useState(false);
	const [generalError, setGeneralError] = useState<string | null>(null);
	const [touchedFields, setTouchedFields] = useState<Set<FieldKey>>(new Set());


	useEffect(() => {
		if (profile && isSuccess) {
			console.log('Setting user in store:', profile);
			dispatch(actions.setUser(profile));
			navigate('/');
		}
	}, [profile, isSuccess, dispatch, navigate, profileError]);

	const validateField = (key: FieldKey, value: string): string | undefined => {
		// Required field validation
		const requiredError = validateRequired(value);
		if (requiredError) return requiredError;

		// Field-specific validation
		if (key === 'email') {
			return validateEmail(value);
		}

		return undefined;
	};

	const validateForm = (): boolean => {
		const newErrors: ValidationErrors = {};

		Object.keys(form).forEach((key) => {
			const value = form[key as keyof ILoginRequest];
			const error = validateField(key as FieldKey, value);
			if (error) {
				newErrors[key as keyof ILoginRequest] = error;
			}
		});

		setErrors(newErrors);
		return Object.keys(newErrors).length === 0;
	};

	const handleChange = (key: FieldKey, value: string) => {
		setForm((prev) => ({ ...prev, [key]: value }));
		if (touchedFields.has(key) || submitAttempted) {
			const error = validateField(key, value);
			setErrors((prev) => ({
				...prev,
				[key]: error
			}));
		}
		setGeneralError(null);
	};

	const handleBlur = (key: FieldKey) => {
		setTouchedFields((prev) => new Set(prev).add(key));
		const value = form[key];
		const error = validateField(key, value);
		setErrors((prev) => ({
			...prev,
			[key]: error
		}));
	};

	const handleSubmit = async () => {
		setSubmitAttempted(true);
		setGeneralError(null);

		if (!validateForm()) {
			return;
		}

		try {
			console.log('Attempting login...');
			await login(form).unwrap();
			dispatch(actions.setCredentials());
		} catch (err: any) {
			console.error('Login error:', err);
			if (err.data && typeof err.data === 'object') {
				const serverErrors: ValidationErrors = {};
				Object.entries(err.data).forEach(([key, value]) => {
					if (Array.isArray(value)) {
						serverErrors[key as keyof ILoginRequest] = value[0];
					} else if (typeof value === 'string') {
						serverErrors[key as keyof ILoginRequest] = value;
					}
				});
				setErrors(serverErrors);
			} else {
				setGeneralError(typeof err.data === 'string' ? err.data : 'Неверный email или пароль');
			}
		}
	};

	const getFieldError = (key: FieldKey): string | undefined => {
		return errors[key];
	};

	if (isAuthenticated) {
		return <Navigate to='/' />;
	}

	return (
		<main className={cls.login}>
			<Header />
			<section className={cls.logModal}>
				<h1 className={cls.title}>Вход</h1>
				{fields.map(({ key, ...rest }, index) => (
					<BaseInput
						key={index}
						value={form[key]}
						onChange={(e) => handleChange(key, e.target.value)}
						onBlur={() => handleBlur(key)}
						error={getFieldError(key)}
						disabled={isLoading}
						{...rest}
					/>
				))}
				<Button text={isLoading ? 'Вход...' : 'Войти'} onClick={handleSubmit} primary disabled={isLoading} style={{ marginTop: '14px' }} />
				{generalError && <div className={cls.error}>{generalError}</div>}
			</section>
			<nav className={cls.nav}>
				<Link to="/auth/reg" className={cls.link}>
					Нет аккаунта? Зарегистрироваться
				</Link>
			</nav>
		</main>
	);
};
