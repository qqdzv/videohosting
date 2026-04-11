export type FieldKey = 'username' | 'email' | 'password' | 'first_name' | 'last_name';

interface Field {
	type: string;
	key: FieldKey;
	placeholder: string;
    label: string;
}
const fields: Field[] = [
	{
		type: 'text',
		key: 'username',
		placeholder: 'Введите имя пользователя',
        label: 'Имя пользователя'
	},
	{
		type: 'text',
		key: 'first_name',
		placeholder: 'Введите фамилию',
        label: 'Фамилия'
	},
	{
		type: 'text',
		key: 'last_name',
		placeholder: 'Введите имя',
        label: 'Имя'
	},
	{
		type: 'email',
		key: 'email',
		placeholder: 'Введите почту',
        label: 'Почта'
	},
];
export default fields;