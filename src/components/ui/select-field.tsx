import * as Select from '@radix-ui/react-select'
import { useRef } from 'react'
import { Check, ChevronDown, ChevronUp, X } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import { cn } from '@/lib/utils'

export type SelectOption = { value: string; label: string; icon?: LucideIcon }
type Props = {
  label: string
  value: string
  options: SelectOption[]
  onValueChange: (value: string) => void
  icon?: LucideIcon
  variant?: 'field' | 'capsule'
  disabled?: boolean
  removable?: boolean
}
// Radix items require non-empty values; the public API keeps the existing empty filter value.
const EMPTY = '__educalibre_empty__'

export function SelectField({ label, value, options, onValueChange, icon: Icon, variant = 'field', disabled = false, removable = false }: Props) {
  const trigger = useRef<HTMLButtonElement>(null)
  const selected = options.find(option => option.value === value)
  const active = variant === 'capsule' && !!value
  const text = variant === 'capsule' ? `${label}${active ? ` · ${selected?.label ?? value}` : ''}` : selected?.label ?? 'Selecciona una oportunidad'
  return <span className={cn('select-shell', `select-${variant}`)} data-active={active || undefined} data-disabled={disabled || undefined}>
    <Select.Root value={value || EMPTY} onValueChange={next => onValueChange(next === EMPTY ? '' : next)} disabled={disabled}>
      <Select.Trigger ref={trigger} className="select-trigger" aria-label={label} title={text}>
        {Icon && <Icon className="select-leading-icon" size={18} aria-hidden="true" />}
        <span className="select-value"><Select.Value>{text}</Select.Value></span>
        <Select.Icon className="select-indicator"><ChevronDown size={16} aria-hidden="true" /></Select.Icon>
      </Select.Trigger>
      <Select.Portal>
        <Select.Content className="select-menu" position="popper" sideOffset={8} collisionPadding={12} align="start" aria-label={label}>
          <Select.ScrollUpButton className="select-scroll"><ChevronUp size={16} aria-hidden="true" /></Select.ScrollUpButton>
          <Select.Viewport className="select-options">
            {options.map(option => {
              const OptionIcon = option.icon ?? Icon
              return <Select.Item key={option.value} value={option.value || EMPTY} textValue={option.label} className="select-option">
                {OptionIcon && <OptionIcon className="select-option-icon" size={18} aria-hidden="true" />}
                <Select.ItemText>{option.label}</Select.ItemText>
                <Select.ItemIndicator className="select-check"><Check size={17} aria-hidden="true" /></Select.ItemIndicator>
              </Select.Item>
            })}
          </Select.Viewport>
          <Select.ScrollDownButton className="select-scroll"><ChevronDown size={16} aria-hidden="true" /></Select.ScrollDownButton>
          <Select.Arrow className="select-menu-arrow" width={14} height={7} />
        </Select.Content>
      </Select.Portal>
    </Select.Root>
    {active && removable && <button type="button" className="select-clear" aria-label={`Quitar filtro ${label}`} title={`Quitar filtro ${label}`} disabled={disabled} onClick={() => { onValueChange(''); trigger.current?.focus() }}><X size={15} aria-hidden="true" /></button>}
  </span>
}
