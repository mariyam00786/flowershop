import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import Button from '../components/ui/Button'

const schema = yup.object().shape({
  email: yup.string().email('Enter a valid email').required('Email is required'),
  username: yup.string().required('Name is required'),
  password: yup.string().min(8, 'Password must be at least 8 characters').required('Password is required'),
  passwordConfirm: yup.string().oneOf([yup.ref('password')], 'Passwords must match').required('Confirm your password'),
})

export default function Register() {
  const { register, handleSubmit, formState: { errors } } = useForm({ resolver: yupResolver(schema) })

  const onSubmit = (data) => {
    console.log(data)
  }

  return (
    <main className="px-6 py-12 md:px-10">
      <div className="mx-auto max-w-md rounded-[2rem] bg-white p-10 shadow-[0_35px_80px_rgba(27,58,45,0.08)]">
        <h1 className="text-3xl font-playfair text-primary">Register</h1>
        <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-6">
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-charcoal/80">Name</label>
            <input type="text" {...register('username')} className="w-full rounded-3xl border border-slate-300 bg-offwhite/90 px-4 py-3 text-sm" />
            {errors.username && <p className="text-sm text-red-600">{errors.username.message}</p>}
          </div>
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-charcoal/80">Email</label>
            <input type="email" {...register('email')} className="w-full rounded-3xl border border-slate-300 bg-offwhite/90 px-4 py-3 text-sm" />
            {errors.email && <p className="text-sm text-red-600">{errors.email.message}</p>}
          </div>
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-charcoal/80">Password</label>
            <input type="password" {...register('password')} className="w-full rounded-3xl border border-slate-300 bg-offwhite/90 px-4 py-3 text-sm" />
            {errors.password && <p className="text-sm text-red-600">{errors.password.message}</p>}
          </div>
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-charcoal/80">Confirm Password</label>
            <input type="password" {...register('passwordConfirm')} className="w-full rounded-3xl border border-slate-300 bg-offwhite/90 px-4 py-3 text-sm" />
            {errors.passwordConfirm && <p className="text-sm text-red-600">{errors.passwordConfirm.message}</p>}
          </div>
          <Button type="submit" className="w-full">Create Account</Button>
        </form>
      </div>
    </main>
  )
}
