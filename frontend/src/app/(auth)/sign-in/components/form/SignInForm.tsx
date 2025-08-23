'use client';

import { Form } from '@/app/components/form/Form';
import { SubmitHandler, useForm } from 'react-hook-form';

type FormValues = {
  identifier: string;
  password: string;
};

export default function SignInForm() {
  const methods = useForm<FormValues>({
    mode: 'onChange',
    defaultValues: {
      identifier: '',
      password: '',
    },
  });
  const onSubmit: SubmitHandler<FormValues> = (data: FormValues) => {
    console.log('Form data:', data);
  };

  return (
    <div>
      <Form
        methods={methods}
        onSubmit={onSubmit}
        className="w-full max-w-xs flex flex-col gap-5"
      >
        <input />
        <input />
        <button type="submit">Sign In</button>
      </Form>
    </div>
  );
}