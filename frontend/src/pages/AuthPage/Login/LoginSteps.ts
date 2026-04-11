export type FieldKey = 'email' | 'password';

interface Field {
	type: string;
	key: FieldKey;
	placeholder: string;
}
const fields: Field[] = [
	{
		type: 'email',
		key: 'email',
		placeholder: 'Email'
	},
	{
		type: 'password',
		key: 'password',
		placeholder: 'Пароль'
	}
];
export default fields;
