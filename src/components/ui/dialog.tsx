import * as Primitive from '@radix-ui/react-dialog'
import { X } from 'lucide-react'
import type { ComponentProps } from 'react'
import { useRef } from 'react'
import { cn } from '@/lib/utils'
export const Dialog = Primitive.Root
export const DialogTitle = Primitive.Title
export const DialogDescription = Primitive.Description
export function DialogContent({ children, className, onOpenAutoFocus, onCloseAutoFocus, ...props }: ComponentProps<typeof Primitive.Content>) {
  const returnFocus = useRef<HTMLElement | null>(null)
  return <Primitive.Portal><Primitive.Overlay className="dialog-overlay" /><Primitive.Content className={cn('dialog-content', className)} {...props} onOpenAutoFocus={event => { returnFocus.current = document.activeElement instanceof HTMLElement ? document.activeElement : null; onOpenAutoFocus?.(event) }} onCloseAutoFocus={event => { onCloseAutoFocus?.(event); if (!event.defaultPrevented) { event.preventDefault(); returnFocus.current?.focus() } }}>{children}<Primitive.Close className="dialog-close" aria-label="Cerrar detalles"><X size={20} /></Primitive.Close></Primitive.Content></Primitive.Portal>
}
