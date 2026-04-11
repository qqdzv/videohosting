export type FieldKey = 'username' | 'email' | 'password' | 'first_name' | 'last_name';

interface Field {
	type: string;
	key: FieldKey;
	placeholder: string;
}
const fields: Field[] = [
	{
		type: 'text',
		key: 'username',
		placeholder: 'Имя пользователя'
	},
	{
		type: 'text',
		key: 'first_name',
		placeholder: 'Фамилия'
	},
	{
		type: 'text',
		key: 'last_name',
		placeholder: 'Имя'
	},
	{
		type: 'email',
		key: 'email',
		placeholder: 'Почта'
	},
	{
		type: 'password',
		key: 'password',
		placeholder: 'Пароль'
	}
];
export default fields;
