export type InspectionPoint={id:string;text:string;allowsNa:boolean;required:boolean}
export type InspectionSection={title:string;points:InspectionPoint[]}
export type InspectionTemplate={code:string;name:string;title:string;reminders:string[];sections:InspectionSection[]}
export const meuleuseTemplate:InspectionTemplate={code:'MEULEUSE',name:'Meuleuse',title:'MEULEUSE : points de vérification avant utilisation',reminders:['Utilisez un disque adapté aux travaux à réaliser et à la meuleuse.','La pièce à découper doit être stable. Serrez-la si nécessaire.',"Il ne doit rien y avoir d'inflammable à proximité.","Vérifiez que vous ne risquez pas d'endommager un réseau (électrique, gaz, eau...).",'Portez les EPI indiqués par le fabricant.',"Attendez l'arrêt complet du disque avant de reposer la meuleuse."],sections:[
{title:'État extérieur',points:[['c1',"Le corps de la meuleuse n'est pas endommagé."],['c2',"Il n'y a pas de vis manquantes."]].map(([id,text])=>({id,text,allowsNa:true,required:true}))},
{title:'Disque',points:[['c3','Le disque est en bon état apparent.'],['c4',"Il n'est pas périmé."],['c5','Il est monté dans le bon sens de rotation et bien fixé.']].map(([id,text])=>({id,text,allowsNa:true,required:true}))},
{title:'Équipement',points:[['c6','Le carter de protection du disque est présent.'],['c7','Il est correctement fixé.'],['c8','La poignée est présente.'],['c9',"Le tube d'évacuation éventuel n'est pas obstrué." ]].map(([id,text])=>({id,text,allowsNa:true,required:true}))},
{title:"Câble d'alimentation",points:[['c10',"Le câble d'alimentation éventuel est en bon état."]].map(([id,text])=>({id,text,allowsNa:true,required:true}))},
{title:'Batterie',points:[['c11',"La batterie éventuelle n'est ni déformée, ni gonflée, ni percée, ni chaude avant utilisation."],['c12',"Elle s'installe et se retire facilement."],['c13',"Il n'y a pas d'écoulement."]].map(([id,text])=>({id,text,allowsNa:true,required:true}))},
{title:'Réglages',points:[['c14','Le réglage éventuel de la vitesse fonctionne.']].map(([id,text])=>({id,text,allowsNa:true,required:true}))},
{title:'Fonctionnement',points:[['c15','La meuleuse fonctionne correctement.']].map(([id,text])=>({id,text,allowsNa:true,required:true}))}
]}
export const genericTemplate:InspectionTemplate={code:'GENERIC',name:'Contrôle générique',title:'CONTRÔLE GÉNÉRIQUE : points de vérification avant utilisation',reminders:[],sections:[{title:'État général',points:[
{id:'g1',text:"L'équipement ne présente pas de détérioration visible.",allowsNa:false,required:true},
{id:'g2',text:'Les protections et dispositifs de sécurité sont présents et en bon état.',allowsNa:true,required:true},
{id:'g3',text:"L'alimentation, le câble, la fiche ou la batterie sont en bon état.",allowsNa:true,required:true},
{id:'g4',text:'Les commandes et dispositifs d’arrêt fonctionnent correctement.',allowsNa:true,required:true},
{id:'g5',text:'Les accessoires et éléments de fixation sont adaptés et correctement fixés.',allowsNa:true,required:true},
{id:'g6',text:"Les marquages et l'identification de l'équipement sont lisibles.",allowsNa:false,required:true}
]}]}

export const templateByEquipmentId:Record<string,InspectionTemplate>={'VMA-0248':meuleuseTemplate}
export function resolveInspectionTemplate(equipmentId:string){return templateByEquipmentId[equipmentId]??genericTemplate}
