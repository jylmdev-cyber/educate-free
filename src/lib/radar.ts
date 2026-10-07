export type RadarCheck = { id: string; url: string; checked_at: string; state: 'baseline' | 'changed' | 'unchanged' | 'access_failure' }
export type RadarReport = { version: 1; checked_at: string | null; checks: RadarCheck[] }
export function parseRadarReport(value: unknown): RadarReport {
  if (!value || typeof value !== 'object' || !('version' in value) || value.version !== 1 || !('checks' in value) || !Array.isArray(value.checks) || !('checked_at' in value) || (value.checked_at !== null && (typeof value.checked_at !== 'string' || !Number.isFinite(Date.parse(value.checked_at))))) throw new Error('Informe de radar inválido')
  if (value.checks.length > 20) throw new Error('Demasiadas señales de radar')
  const checks: RadarCheck[] = value.checks.map((item: unknown) => {
    if (!item || typeof item !== 'object' || !('id' in item) || typeof item.id !== 'string' || !('url' in item) || typeof item.url !== 'string' || !('checked_at' in item) || typeof item.checked_at !== 'string' || !Number.isFinite(Date.parse(item.checked_at)) || !('state' in item) || !['baseline', 'changed', 'unchanged', 'access_failure'].includes(String(item.state))) throw new Error('Señal de radar inválida')
    return { id: item.id, url: item.url, checked_at: item.checked_at, state: item.state as RadarCheck['state'] }
  })
  return { version: 1, checked_at: value.checked_at as string | null, checks }
}
